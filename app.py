import requests
import logging
from itertools import cycle
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from auth_utils import token_required
from config import NODES, GATEWAY_PORT

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gateway")
node_cycle = cycle(NODES)


def get_next_active_node():
    for _ in range(len(NODES)):
        node = next(node_cycle)
        try:
            requests.get(f"{node}/health", timeout=0.5)
            return node
        except requests.exceptions.RequestException:
            logger.warning(f"Node {node} is down.")
            continue
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    import os
    from auth_utils import generate_token
    data = request.json
    admin_user = os.environ.get('ADMIN_USER', 'admin')
    admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin')
    if data.get('username') == admin_user and data.get('password') == admin_pass:
        return jsonify({"token": generate_token('admin')})
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@token_required
def proxy(path):
    target_node = get_next_active_node()
    if not target_node:
        return jsonify({"error": "No available workers"}), 503

    url = f"{target_node}/{path}"

    excluded_headers = ['Host', 'Content-Length']
    headers = {k: v for k, v in request.headers if k not in excluded_headers}

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            json=request.get_json(silent=True),
            timeout=5
        )
        return Response(resp.content, resp.status_code, dict(resp.headers))

    except requests.exceptions.RequestException as e:
        logger.error(f"Upstream error: {e}")
        return jsonify({"error": "Upstream service failed"}), 502


if __name__ == '__main__':
    print(f"Gateway running on http://127.0.0.1:{GATEWAY_PORT}")
    app.run(port=GATEWAY_PORT, debug=True)