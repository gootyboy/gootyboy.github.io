from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, request, redirect, session

db = SQL("sqlite:///spanish_dict.db")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

user_details = {"username": "GPulugurta", "password": "Spanish_dict@LOGIN"}


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/loggedin", methods=["GET", "POST"])
def index_login():
    if session["user details"] == user_details:
        return render_template("index_login.html")
    return redirect("/login")


@app.route("/login/incorrect", methods=["GET", "POST"])
def incorrect():
    return render_template("login_fail.html")


@app.route("/loggedin/add", methods=["POST"])
def add():
    return render_template("add.html")


@app.route("/addword", methods=["POST"])
def add_word():
    en_word = request.form.get("english")
    sp_word = request.form.get("spanish")
    row_type = request.form.get("type")
    print(row_type)
    if en_word != None and sp_word != None:
        db.execute(
            "INSERT INTO words (type, spanish, english) VALUES(?, ?, ?)",
            row_type,
            sp_word,
            en_word,
        )

    return redirect("/loggedin/see")


@app.route("/loggedin/see", methods=["POST", "GET"])
def see_login():
    words = db.execute("SELECT * FROM words")
    return render_template("see_login.html", words=words)


@app.route("/remove", methods=["POST"])
def remove():
    id = request.form.get("id")
    db.execute("DELETE FROM words WHERE id = ?", id)

    return redirect("/loggedin/see")


@app.route("/see", methods=["POST", "GET"])
def see():
    words = db.execute("SELECT * FROM words")
    return render_template("see.html", words=words)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user details"] = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }
        return redirect("/loggedin")
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["user details"] = None
    return redirect("/")
