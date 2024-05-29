from flask import redirect, render_template, request, session

from flask_app import app
from flask_app.controllers.check_user import check_doctor
from flask_app.models.appointment import Appointment
from flask_app.models.news import News
from flask_app.models.patient_info import Patient_Cartel
from flask_app.models.shift import Shift
from flask_app.models.testimonial import Testimonial
from flask_app.models.user import User


@app.route("/doctor")
def doctor():
    check = check_doctor(session)
    if check:
        return check

    user = User.get_user_by_id({"id": session['user_id']})
    doctor_nr = User.get_total_nr_of_doctors()
    staff = User.get_total_nr_of_staff()
    patients = User.get_total_nr_of_patients()
    news = News.get_all_news()
    my_doctor = User.get_doctor()
    testimonials = Testimonial.get_all_testimonials()

    return render_template(
        "doctor/doctor.html",
        user=user,
        doctor=doctor_nr,
        staff=staff,
        patients=patients,
        news=news,
        mydoctor=my_doctor,
        testimonials=testimonials
    )


@app.route("/patient/cartel")
def cartel():
    check = check_doctor(session)
    if check:
        return check
    patients = User.get_all_patients()
    return render_template(
        "doctor/patientCartel.html", patients=patients
    )


@app.route("/patient/<int:user_id>", methods=["GET", "POST"])
def patient_info(user_id):
    check = check_doctor(session)
    if check:
        return check
    if request.method == "POST":
        check_doctor(session)
        data = {
            "examinate": request.form["examinate"],
            "treatment": request.form["treatment"],
            "medicalReport": request.form["medicalReport"],
            "summary": request.form["summary"],
            "writer": session['user_id'],
            "patient_id": user_id
        }

        patient_data = {
            "patient_id": id,
            "age": request.form["age"],
            "gender": request.form["gender"]
        }
        if User.validate_patient(patient_data):
            User.update_patient(patient_data)

        if Patient_Cartel.validate_cartel(data):
            Patient_Cartel.insert_cartel(data)
        patient = User.get_user_by_id({"id": id})
        cartels = Patient_Cartel.get_cartel_by_id({"patient_id": id})
        return render_template(
            "doctor/patient_info.html", patient=patient, cartels=cartels
        )
    else:
        check_doctor(session)
        patient = User.get_user_by_id({"id": id})
        cartels = Patient_Cartel.get_cartel_by_id({"patient_id": id})
        return render_template(
            "doctor/patient_info.html", patient=patient, cartels=cartels
        )


@app.route("/colleague")
def colleague():
    check = check_doctor(session)
    if check:
        return check
    doctors = User.get_all_doctors()
    nurses = User.get_all_nurses()

    return render_template(
        "doctor/colleague.html", doctors=doctors, nurses=nurses
    )


@app.route("/appointement")
def appointment():
    check = check_doctor(session)
    if check:
        return check
    appointments = Appointment.get_all_appointments({"doctor_id": session['user_id']})
    shifts = Shift.get_shift_by_user_id({"id": session['user_id']})
    return render_template(
        "doctor/appointment.html", appointments=appointments, shifts=shifts
    )


@app.route("/shift/<int:user_id>")
def shift(user_id):
    check = check_doctor(session)
    if check:
        return check
    get_shifts = Shift.get_shift_by_id({"id": user_id})

    if Shift.validate_shift(get_shifts):
        Shift.confirm_shift({"id": id})
    return redirect("/appointement")


@app.route("/appointement/<int:appointment_id>")
def view_appointment(appointment_id):
    check = check_doctor(session)
    if check:
        return check
    appointments = Appointment.get_appointment_by_id({"id": appointment_id})
    return render_template(
        "doctor/view_appointment.html", appointments=appointments
    )


@app.route("/edit_appointement/<int:appointment_id>")
def edit_appointment(appointment_id):
    check = check_doctor(session)
    if check:
        return check
    appointments = Appointment.get_appointment_by_id({"id": appointment_id})
    return render_template(
        "doctor/edit_appointment.html", appointments=appointments
    )


@app.route("/edit_appointment_datetime/<int:appointment_id>", methods=["POST"])
def edit_appointment_datetime(appointment_id):
    check = check_doctor(session)
    if check:
        return check
    data = {
        "appointment_id": appointment_id,
        "date": request.form["date"],
        "time": request.form["time"]
    }
    if Appointment.validate_date_time(data):
        Appointment.update_appointment_datetime(data)
    return redirect("/appointement")


@app.route("/cancel_appointement/<int:appointment_id>")
def cancel_appointment(appointment_id):
    check = check_doctor(session)
    if check:
        return check
    Appointment.cancel_appointment({"id": appointment_id})
    return redirect("/appointement")

