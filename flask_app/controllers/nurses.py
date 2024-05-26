from flask import render_template, session

from flask_app import app
from flask_app.controllers.check_user import check_nurse
from flask_app.models.news import News
from flask_app.models.testimonial import Testimonial
from flask_app.models.user import User


@app.route("/nurse")
def nurse():
    check = check_nurse(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session['user_id']})
    testimonials = Testimonial.get_all_testimonials()
    news = News.get_all_news()
    return render_template(
        "nurse/nurse.html",
        user=user,
        testimonials=testimonials,
        news=news
    )


@app.route("/nurse/patient")
def nurse_patients_cartel():
    check = check_nurse(session)
    if check:
        return check
    patients = User.get_all_patients()
    return render_template("nurse/patients.html", patients=patients)


@app.route("/nursePatient/<int:patient_id>")
def check_patient_cartel(patient_id):
    check = check_nurse(session)
    if check:
        return check
    return render_template("nurse/patientCartel.html")


@app.route("/nurse/colleague")
def nurse_colleague():
    check = check_nurse(session)
    if check:
        return check
    doctors = User.get_all_doctors()
    pharmacists = User.get_all_pharmacists()
    nurses = User.get_all_nurses()
    return render_template(
        "nurse/colleague.html",
        doctors=doctors,
        pharmacists=pharmacists,
        nurses=nurses
    )
