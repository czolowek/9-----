from uuid import uuid4

from flask import Flask, render_template, redirect, request, url_for, flash

from db.base import Session, create_db
from db.models import Room


app = Flask(__name__)
app.secret_key = "password"


@app.route("/add_room/", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        with Session() as session:
            number = request.form.get("number")
            floor = request.form.get("floor")
            type = request.form.get("type")
            square = request.form.get("square")
            img_name_origin = None
            img_name = None
            img_url = None

            file = request.files.get("img")
            if file and file.filename:
                img_name_origin = file.filename
                img_name = uuid4().hex + "." + img_name_origin.split(".")[-1]
                img_url = f"static/img/{img_name}"
                file.save(img_url)

            room = Room(
                number=number,
                floor=floor,
                type=type,
                square=square,
                img_name_origin=img_name_origin,
                img_name=img_name,
                img_url=img_url
            )
            session.add(room)
            session.commit()
            flash("Кімната успішно додана")
            return redirect(url_for("index"))

    return render_template("add_room.html")


@app.get("/")
def index():
    with Session() as session:
        rooms = session.query(Room).all()
        return render_template("index.html", rooms=rooms)


@app.get("/room/<int:room_id>")
def get_room(room_id: int):
    with Session() as session:
        room = session.query(Room).where(Room.id == room_id).first()
        return render_template("room.html", room=room)


@app.route("/edit_room/<int:room_id>", methods=["GET", "POST"])
def edit_room(room_id: int):
    with Session() as session:
        room = session.query(Room).where(Room.id == room_id).first()

        if request.method == "POST":
            room.number = request.form.get("number")
            room.floor = request.form.get("floor")
            room.type = request.form.get("type")
            room.square = request.form.get("square")
            room.reserved = True if request.form.get("reserved") else False

            file = request.files.get("img")
            if file and file.filename:
                room.img_name_origin = file.filename
                room.img_name = uuid4().hex + "." + file.filename.split(".")[-1]
                room.img_url = f"static/img/{room.img_name}"
                file.save(room.img_url)

            session.commit()
            flash("Інформацію про кімнату успішно оновлено")
            return redirect(url_for("get_room", room_id=room_id))

        return render_template("edit_room.html", room=room)


@app.get("/del_room/<int:room_id>")
def del_room(room_id: int):
    with Session() as session:
        room = session.query(Room).where(Room.id == room_id).first()
        session.delete(room)
        session.commit()
        flash(f"Кімнату з номером {room.number} успішно видалено")
        return redirect(url_for("index"))


@app.get("/reserve/<int:room_id>/")
def reserve(room_id: int):
    with Session() as session:
        room = session.query(Room).where(Room.id == room_id).first()
        room.reserved = True
        session.commit()
        flash("Кімната успішно зарезервована")
        return redirect(url_for("get_room", room_id=room_id))


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=8080)
