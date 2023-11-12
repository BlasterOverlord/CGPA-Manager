from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps

db = SQL("sqlite:///data.db")

def get_key_semester(dict):
    return dict['semester']


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def max_semesters(id):
    max = db.execute("SELECT semesters FROM target WHERE user_id = ?", id)

    if max:
        return max[0]["semesters"]
    else:
        return 8


def current_semesters(id):
    listOfSems = db.execute("SELECT semester FROM profile WHERE user_id = ?", id)
    if listOfSems:
        #finding the dict that has the max value
        max_dict = max (listOfSems, key=get_key_semester)
        return max_dict['semester'] #return current max semester number
    else:
        return 0



def calculate_gpa(user_id, semester_id):
    semester_data = db.execute("SELECT credit,gpa FROM profile WHERE user_id = ? AND semester = ?", user_id, semester_id)

    if not semester_data:
        return 0
    else:
        # calculation: (SUMMATION(credit*gpa)) / (total credits)
        sum = 0
        totalCredits = 0
        for row in semester_data:
            sum += row["credit"] * row["gpa"]
            totalCredits += row["credit"]

        gpa = sum/totalCredits
        return gpa


def calculate_cgpa(id):
    current_max = current_semesters(id)
    if current_max <= 0:
        return 0
    # calculation: SUMMATION(gpa)/current max semester

    gpa_sum = 0
    for i in range(current_max):
        gpa_sum += calculate_gpa(id, i+1)

    cgpa = gpa_sum / current_max
    return cgpa


def required_gpa(id):
    max = max_semesters(id)
    current = current_semesters(id)
    semesters_left = max - current

    if semesters_left <= 0:
        return "Congrats on graduating!"
    else:
        # calculation: ( (target cgpa * max semester) - (current cgpa) ) / remaining semesters
        target = db.execute("SELECT cgpa FROM target WHERE user_id = ?", id)
        cgpa = calculate_cgpa(id)
        required = ( (target[0]["cgpa"] * max) - (cgpa * current) ) / (semesters_left)

        if required < 0 or required > 4:
            return "Not possible :("
        else:
            return "Get " + str(round(required,2)) + " GPA each semester"
