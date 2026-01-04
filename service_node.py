import argparse
from flask import Flask, request, jsonify
from bson import ObjectId
from db_manager import db_instance

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    if db_instance.is_alive():
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "db_down"}), 500


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(db_instance.get_collection('tasks').find())
    return jsonify([db_instance.serialize_doc(t) for t in tasks]), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        "title": data.get("title"),
        "description": data.get("description", ""),
        "status": data.get("status", "todo")
    }
    res = db_instance.get_collection('tasks').insert_one(new_task)
    return jsonify(
        db_instance.serialize_doc(db_instance.get_collection('tasks').find_one({"_id": res.inserted_id}))), 201


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    try:
        task = db_instance.get_collection('tasks').find_one({"_id": ObjectId(id)})
        if task:
            return jsonify(db_instance.serialize_doc(task)), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400


@app.route('/tasks/<id>', methods=['PUT', 'PATCH'])
def update_task(id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if k != 'id'}

    try:
        result = db_instance.get_collection('tasks').find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_fields},
            return_document=True
        )
        if result:
            return jsonify(db_instance.serialize_doc(result)), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        res = db_instance.get_collection('tasks').delete_one({"_id": ObjectId(id)})
        if res.deleted_count > 0:
            return jsonify({"message": "Deleted"}), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()

    print(f"Starting Service Node on port {args.port}")
    app.run(port=args.port, debug=False)