from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.news import News
from flask_app.models.testimonial import Testimonial

from flask_app.models.shift import Shift



@app.route("/doctor")
def doctor():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user['role'] != "D435":
        return redirect("/")
    doctor = User.get_total_nr_of_doctors()
    staff = User.get_total_nr_of_staff()
    patients = User.get_total_nr_of_patients()
    news = News.get_all_news()
    mydoctor = User.get_doctor()
    testimonials = Testimonial.get_all_testimonials()
    return render_template("doctor.html", user=user, doctor=doctor , staff=staff, patients=patients, news=news, mydoctor=mydoctor, testimonials=testimonials)  

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user['role'] != "D435":
        return redirect("/")
    return render_template("profile.html", user=user)

@app.route("/patient/cartel")
def cartel():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user['role'] != "D435":
        return redirect("/")
    patients = User.get_all_patients()
    return render_template("patientCartel.html" , patients=patients)


@app.route("/colleague")
def colleague():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['role'] != "D435":
        return redirect("/")
    doctors = User.get_all_doctors() 
    pharmacists = User.get_all_pharmacists()
    nurses = User.get_all_nurses()
    return render_template("colleague.html", doctors=doctors, pharmacists=pharmacists, nurses=nurses)

