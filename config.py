# PROJECT CONFIGURATION
# For default deployment, do not change macro values
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "todo_db"
SECRET_KEY = os.environ.get("SECRET_KEY", "default_key") # !!! Store in ENV when in prod

GATEWAY_PORT = 5000

_nodes_env = os.environ.get("NODES")
if _nodes_env:
    NODES = _nodes_env.split(",")
else:
    NODES = ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]