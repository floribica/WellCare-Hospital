from flask import request, session, redirect, flash

from flask_app import app
from flask_app.models.application import Application


@app.route("/application", methods=["POST"])
def application():
    if "user_id" in session:
        return redirect("/check")

    data = {
        "fullName": request.form["fullName"],
        "email": request.form["email"],
        "role": request.form["role"]
    }

    if not Application.validate_application(request.form):
        return redirect(request.referrer)

    Application.create_application(data)
    flash("Application submitted successfully!", "applicationSuccess")
    return redirect("/")
