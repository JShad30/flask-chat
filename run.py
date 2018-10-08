import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
messages = []
    
    
def add_messages(username, message):
    """Add messages to the `messages` list"""
    now = datetime.now().strftime("%H:%M:%S")
    message_dict = {"timestamp": now, "from": username, "message": message}
    messages.append(message_dict)
    
    
def get_all_messages():
    """Get al of the messages and separate them by a `br`"""
    return messages


@app.route("/", methods=["GET", "POST"])
def index():
    """Main page with instruction"""
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.write(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")
    
    
@app.route("/<username>")
def user(username):
    """Display Chat messages"""
    message = get_all_messages()
    return render_template("chat.html", username=username, chat_messages=messages)
    
    
@app.route("/<username>/<message>")
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    add_messages(username, message)
    return redirect(username)
    
    
app.run(host=os.getenv('IP'), port=int(os.getenv("PORT")), debug=True)