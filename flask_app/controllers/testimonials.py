from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.testimonial import Testimonial

@app.route("/testimonials/new", methods=["POST"])
def new_testimonial():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    if not Testimonial.validate_testimonial(data):
        return redirect("/")
    
    Testimonial.create_testimonial(data)
    return redirect("/")