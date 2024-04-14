from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.testimonial import Testimonial
from flask_app.controllers.check_user import check_patient


@app.route("/testimonials/new", methods=["POST"])
def new_testimonial():
        
        check_patient(session)
        
        data = {
            "description": request.form["description"],
            "user_id": session["user_id"]
        }
        
        if not Testimonial.validate_testimonial(data):
                return redirect("/")
        
        Testimonial.create_testimonial(data)
        
        return redirect("/")