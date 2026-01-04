const GATEWAY_URL = "http://127.0.0.1:5000";
let jwtToken = null;

async function login() {
    const username = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    try {
        const response = await fetch(`${GATEWAY_URL}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: username, password: pass})
        });

        if (response.ok) {
            const data = await response.json();
            jwtToken = data.token;
            document.getElementById('auth-status').innerText = "Logged In!";
            document.getElementById('auth-status').style.color = "green";
            loadTasks();
        } else {
            alert("Login failed");
        }
    } catch (e) {
        console.error(e);
        alert("Connection error");
    }
}

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`
    };
}


async function loadTasks() {
    if (!jwtToken) return alert("Please login first");

    document.getElementById('loading').style.display = 'block';
    const list = document.getElementById('task-list');
    list.innerHTML = '';

    try {
        const response = await fetch(`${GATEWAY_URL}/tasks`, {
            method: 'GET',
            headers: getHeaders()
        });

        if (response.ok) {
            const tasks = await response.json();
            tasks.forEach(task => {
                const li = document.createElement('li');
                li.style.border = "1px solid #eee";
                li.style.margin = "5px 0";
                li.style.padding = "10px";
                li.innerHTML = `
                    <strong>${task.title}</strong> [${task.status}] <br>
                    <small>${task.description || ''}</small> <br>
                    ID: ${task.id} <br>
                    <button onclick="updateStatus('${task.id}', 'done')">Mark Done</button>
                    <button onclick="deleteTask('${task.id}')">Delete</button>
                `;
                list.appendChild(li);
            });
        } else {
            console.error("Failed to load tasks");
        }
    } catch (e) {
        console.error(e);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

async function createTask() {
    if (!jwtToken) return alert("Please login first");

    const title = document.getElementById('new-title').value;
    const desc = document.getElementById('new-desc').value;
    const status = document.getElementById('new-status').value;

    const response = await fetch(`${GATEWAY_URL}/tasks`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({title, description: desc, status})
    });

    if (response.status === 201) {
        document.getElementById('new-title').value = '';
        document.getElementById('new-desc').value = '';
        loadTasks();
    } else {
        alert("Error creating task");
    }
}

async function updateStatus(id, newStatus) {
    if (!jwtToken) return alert("Please login first");

    await fetch(`${GATEWAY_URL}/tasks/${id}`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({status: newStatus})
    });
    loadTasks();
}

async function deleteTask(id) {
    if (!jwtToken) return alert("Please login first");

    if(confirm("Are you sure?")) {
        await fetch(`${GATEWAY_URL}/tasks/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        loadTasks();
    }
}