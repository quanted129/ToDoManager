# To-Do Manager

A distributed, containerized To-Do List application built with Python, Flask, and MongoDB, including load balancing, authentication, in-built security and sanity checks, and debugging capabilities.

## ⭐ Features

*   **API Gateway:** Central entry point handling authentication and request routing.
*   **Load Balancing:** Distribution of requests across 2 consecutively loaded worker nodes.
*   **Authentication:** JWT-based security (`admin`/`admin` by default).
*   **Persistence:** NoSQL (MongoDB) for data storage.
*   **Containerization:** Fully Dockerized environment using Docker Compose.

## 🛠 Tech Stack

*   **Backend:** Python, Flask
*   **Database:** MongoDB
*   **Frontend:** HTML, JavaScript
*   **Containerization:** Docker Compose

## 💻 Prerequisites

*   [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.
*   (Optional for local run) Python 3.9+ and a local MongoDB server (mongod) instance.

## 🚀 Installation & Running

### Method 1: Docker (Recommended)

The easiest way to run the application is using Docker Compose, which spins up the database, two worker nodes, and the gateway automatically.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/quanted129/ToDoManager
    cd ToDoManager
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    Open your browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

### Method 2: Manual Local Setup

If you prefer running without Docker, ensure MongoDB is running locally on port `27017`.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Service Nodes (in separate terminals):**
    ```bash
    python service_node.py --port 5001
    python service_node.py --port 5002
    ```

3.  **Start the Gateway:**
    ```bash
    python app.py
    ```

4.  **Access the application:**
    Open `http://127.0.0.1:5000` in your browser.

## 👨‍💻 Usage

To interact with the task list, you must first log in via the UI.

**Default Credentials (store yours in .env!):**
*   **Username:** `admin`
*   **Password:** `admin`

## ⚙️ Configuration

Environment variables can be adjusted in docker-compose.yml or config.py:

*    MONGO_URI: Connection string for MongoDB.
*    NODES: Comma-separated list of worker node URLs (e.g., http://node1:5001,http://node2:5002).
*    SECRET_KEY: Key used for encoding (ensure this is changed when using locally).