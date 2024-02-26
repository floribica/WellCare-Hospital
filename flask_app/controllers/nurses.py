from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User


@app.route("/nurse")
def nurse():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    return render_template("nurse.html", user=user)

