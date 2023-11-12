from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, max_semesters, current_semesters, calculate_gpa, calculate_cgpa, required_gpa
from itertools import zip_longest


app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.context_processor
def inject_variables():
    user_id = session.get("user_id")
    if user_id is not None:
        id = session["user_id"]
        current = current_semesters(id)
        return dict(current=current)
    else:
        return {}

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session["user_id"]
    cgpa = calculate_cgpa(id)
    user = db.execute("SELECT * FROM target WHERE user_id = ?", id)
    if not user:
        target = 0
        required = "you must set a target first :p"
        return render_template("index.html", target=target, cgpa=cgpa, required=required)
    else:
        target = user[0]["cgpa"]
        required = required_gpa(id)
        return render_template("index.html", target=target, cgpa=cgpa, required=required)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error = "You must submit a username!"
            return render_template("sorry.html", error=error)

        if not request.form.get("password"):
            error = "You must eneter a password!"
            return render_template("sorry.html", error=error)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error = "Invalid username and/or password."
            return render_template("sorry.html", error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usernames = []
        list = db.execute("SELECT username FROM users;")
        for user in list:
            usernames.append(user["username"])

        if not username:
            error = "Must provide a username!"
            return render_template("sorry.html", error=error)

        if not password or not confirmation:
            error = "Must provide a password and confirm!"
            return render_template("sorry.html", error=error)

        if password != confirmation:
            error = "Passwords don't match!"
            return render_template("sorry.html", error=error)

        if username in usernames:
            error = "Username already exists."
            return render_template("sorry.html", error=error)

        password = generate_password_hash(password, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password)
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/target", methods=["GET", "POST"])
@login_required
def t():
    if request.method == "POST":
        id = session["user_id"]
        cgpa = request.form.get("target")
        semesters = request.form.get("semesters")

        if not cgpa:
            error = "Must provide the cgpa!"
            return render_template("sorry.html", error=error)
        if not semesters:
            error = "Must provide the total no. of semesters!"
            return render_template("sorry.html", error=error)

        rows = db.execute("UPDATE target SET cgpa=?, semesters=? WHERE user_id = ?", cgpa, semesters, id)

        if rows <= 0:
            db.execute("INSERT INTO target(user_id,cgpa,semesters) VALUES(?,?,?)", id, cgpa, semesters)

        return redirect("/")

    else:
        return render_template("target.html")



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":
        id = session["user_id"]
        courses = request.form.getlist("course")
        credits = request.form.getlist("credit")
        gpas = request.form.getlist("gpa")

        current = current_semesters(id)
        current += 1

        for course, credit, gpa in zip_longest(courses, credits, gpas):
            db.execute("INSERT INTO profile(user_id,semester,course,credit,gpa) VALUES(?,?,?,?,?)", id, current, course, credit, gpa)

        return redirect("/")

    else:
        id = session["user_id"]
        current = current_semesters(id)
        max = max_semesters(id)
        if current >= max:
            error = "Maximum semesters exceeded! Please remove a semester first!"
            return render_template("sorry.html", error=error)

        current += 1
        return render_template("add.html", current=current)


@app.route("/semester/<int:semester_id>")
@login_required
def show_semester(semester_id):

    id = session["user_id"]
    current = current_semesters(id)
    semester_data = db.execute("SELECT course,credit,gpa FROM profile WHERE user_id = ? AND semester = ?", id, semester_id)
    gpa = calculate_gpa(id, semester_id)

    return render_template("semester.html", semester_id=semester_id, semester_data=semester_data, gpa=gpa)


@app.route("/delete/<int:semester_id>", methods=["POST"])
@login_required
def delete_semester(semester_id):
    id = session["user_id"]

    db.execute("DELETE FROM profile WHERE user_id = ? AND semester = ?", id, semester_id)

    #updating the numbering of the remaining semesters
    db.execute("UPDATE profile SET semester = semester - 1 WHERE user_id = ? AND semester > ?", id, semester_id)

    return redirect("/")
