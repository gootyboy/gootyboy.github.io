from flask import Flask, render_template, request, redirect
from cs50 import SQL

db = SQL("sqlite:///spanish_dict.db")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index_login.html")

@app.route("/add", methods=["POST"])
def add():
    return render_template("add.html")

@app.route("/addword", methods=["POST"])
def add_word():
    en_word = request.form.get("english")
    sp_word = request.form.get("spanish")
    if en_word != None and sp_word != None:
        db.execute("INSERT INTO words (spanish, english) VALUES(?, ?)", sp_word, en_word)
    
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