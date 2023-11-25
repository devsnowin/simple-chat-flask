import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

from lib import utils

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
socketio = SocketIO(app)

rooms = {}


@app.route('/', methods=["POST", "GET"])
def home_page():
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        room_id = request.form.get("roomId")
        join = request.form.get("join")
        create = request.form.get("create")

        print({"name": name, "room_id": room_id, "join": join, "create": create})

        # validate
        if not name:
            return render_template("home.html", error="Please enter a name", name=name, roomId=room_id)

        if join and not room_id:
            print("join")
            return render_template("home.html", error="Please enter a room id", name=name, roomId=room_id)

        room = room_id

        print(f"rooms: {rooms}")
        print(f"room id: {room_id}")

        if create:
            print("create..")
            room = utils.generate_unique_code(4, rooms, room_id)
            rooms[room] = {"members": 0, "messages": []}
        elif room_id not in rooms:
            return render_template("home.html", error="Room does not exist.", name=name,
                                   roomId=room_id)

        session["room"] = room
        session["name"] = name

        return redirect(url_for("room_page"))

    return render_template("home.html")


@app.route('/room', methods=["GET", "POST"])
def room_page():
    room = session.get("room")
    user = session.get("name")

    print(dict(room=room, name=user))

    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home_page"))

    return render_template("room.html", room=room, user=user, messages=rooms[room]["messages"])


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": "Chat Bot", "message": f"{name.capitalize()} has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} has joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": "Chat Bot", "message": f"{name.capitalize()} has left the room"}, to=room)
    print(f"{name} has left room {room}")


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["message"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')}: {data['message']}")


if __name__ == "__main__":
    app.run(debug=True)
