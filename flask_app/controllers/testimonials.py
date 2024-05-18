from flask import request, session, redirect

from flask_app import app
from flask_app.controllers.check_user import check_patient
from flask_app.models.testimonial import Testimonial


@app.route("/testimonials/new", methods=["POST"])
def new_testimonial():
    check = check_patient(session)
    if check:
        return check
    data = {
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    if not Testimonial.validate_testimonial(data):
        return redirect("/")
    Testimonial.create_testimonial(data)
    return redirect("/")
