from flask import redirect, render_template, request, session

from flask_app import app
from flask_app.controllers.check_user import check_nurse
from flask_app.models.news import News
from flask_app.models.nurse_treatments import Nurse_treatments
from flask_app.models.patient_info import Patient_Cartel
from flask_app.models.shift import Shift
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
    cartels = Patient_Cartel.get_cartel_by_id({"patient_id": patient_id})
    nurse_reports = Nurse_treatments.get_cartel_by_id({"patient_id": patient_id})
    patient = User.get_user_by_id({"id": patient_id})
    return render_template(
        "nurse/patientCartel.html",
        nurse_reports=nurse_reports,
        cartels=cartels,
        patient=patient
    )


@app.route("/nurse/colleague")
def nurse_colleague():
    check = check_nurse(session)
    if check:
        return check
    staff = User.get_all_staff()
    return render_template(
        "nurse/colleague.html",
        staff=staff
    )


@app.route("/nurse/shifts")
def nurse_shifts():
    check = check_nurse(session)
    if check:
        return check
    shifts = Shift.get_shift_by_user_id({"id": session['user_id']})
    return render_template(
        "nurse/shifts.html",
        shifts=shifts
    )


@app.route("/nurse_patient/<int:patient_id>", methods=['POST'])
def add_patient_cartel(patient_id):
    check = check_nurse(session)
    if check:
        return check
    data = {
        "patient_id": patient_id,
        "nurse_id": session['user_id'],
        "temperature": request.form['temperature'],
        "blood_pressure": request.form['blood_pressure'],
        "heart_rate": request.form['heart_rate'],
        "respiratory_rate": request.form['respiratory_rate'],
        "oxygen_saturation": request.form['oxygen_saturation'],
        "pain_level": request.form['pain_level'],
        "notes": request.form['notes']
    }
    if Nurse_treatments.validate_cartel(data):
        Nurse_treatments.add_cartel(data)
    return redirect(f"/nursePatient/{patient_id}")
