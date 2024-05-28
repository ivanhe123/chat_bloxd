
from flask import Flask,request
from flask_socketio import emit
from flask_socketio import SocketIO
import streamlit as st

socketio = SocketIO()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"

socketio.init_app(app)

users = {}
@app.route("/")
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask-SocketIO Example</title>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js" integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+" crossorigin="anonymous"></script>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #e5e5e5;
        }

        #chat {
            width: 50%;
        }

        #chat input {
            width: 99%;
        }

        ul {
            height: 500px;
            background-color: white;
            overflow-y: scroll;
        }

        li {
            list-style: none;
        }

        #landing {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 10px;
        }
    </style>
</head>
<body>
    <div id="landing">
        <input type="text" id="username" placeholder="Username">
        <button id="join-btn">JOIN</button>
    </div>

    <div id="chat" style="display:none;">

        <ul id="chat-messages">
        </ul>
        <input type="text" id="message" placeholder="Enter a Message">
    </div>
    <script>
        const socket = io({autoConnect: false});

        document.getElementById("join-btn").addEventListener("click", function() {
            let username = document.getElementById("username").value;

            socket.connect();

            socket.on("connect", function() {
                socket.emit("user_join", username);
            })

            document.getElementById("chat").style.display = "block";
            document.getElementById("landing").style.display = "none";
        })

        document.getElementById("message").addEventListener("keyup", function (event) {
            if (event.key == "Enter") {
                let message = document.getElementById("message").value;
                socket.emit("new_message", message);
                document.getElementById("message").value = "";
            }
        })

        socket.on("chat", function(data) {
            let ul = document.getElementById("chat-messages");
            let li = document.createElement("li");
            li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
            ul.appendChild(li);
            ul.scrolltop = ul.scrollHeight;
        })
    </script>
</body>
</html>"""
@app.route('/streamlit')
def streamlit():
    st.set_page_config(page_title="My Streamlit App")
    st.write("Hello, world!")
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
