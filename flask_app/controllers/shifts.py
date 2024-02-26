from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.shift import Shift

@app.route("/doctor/shift")
def doctor_shift():
    return render_template("doctor_shifts.html")

@app.route("/doctor/shift/process", methods=["POST"])
def doctor_shift_process():
    data = {
        "start": request.form["start"],
        "end": request.form["end"],
        "user_id": request.form['user_id']
    }
    Shift.create_shift(data)
    return redirect("/doctor")