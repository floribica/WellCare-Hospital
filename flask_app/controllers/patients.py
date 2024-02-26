from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.news import News
from flask_app.models.shift import Shift


@app.route("/patient")
def patient():
    if "user_id" not in session:
        return redirect("/check")
   
    return render_template("patient.html")