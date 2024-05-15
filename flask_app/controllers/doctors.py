from flask import redirect, render_template, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.news import News
from flask_app.models.testimonial import Testimonial
from flask_app.models.patient_info import Patient_Cartel
from flask_app.controllers.check_user import check_doctor


# open doctor page
@app.route("/doctor")
def doctor():
        check_doctor(session)

        user = User.get_user_by_id({"id": session['user_id']})
        doctor = User.get_total_nr_of_doctors()
        staff = User.get_total_nr_of_staff()
        patients = User.get_total_nr_of_patients()
        news = News.get_all_news()
        mydoctor = User.get_doctor()
        testimonials = Testimonial.get_all_testimonials()

        return render_template("doctor.html", user=user, doctor=doctor , staff=staff, patients=patients, news=news, mydoctor=mydoctor, testimonials=testimonials)  


# open doctor profile
@app.route("/profile")
def profile():
        check_doctor(session)
        user = User.get_user_by_id({"id": session['user_id']})
        return render_template("profile.html", user=user)


# open patient cartels for the doctor
@app.route("/patient/cartel")
def cartel():
        check_doctor(session)
        patients = User.get_all_patients()
        return render_template("patientCartel.html" , patients=patients)


# open patient cartel for the doctor
@app.route("/patient/<int:id>", methods=["GET", "POST"])
def patient_info(id):
        if request.method == "POST":
                check_doctor(session)
                data = {
                        "examinate": request.form["examinate"],
                        "treatment": request.form["treatment"],
                        "medicalReport": request.form["medicalReport"],
                        "summary": request.form["summary"],
                        "writer": session['user_id'],
                        "patient_id": id
                }
                
                patient_data = {
                        "patient_id": id,
                        "birthday": request.form["birthday"],
                        "gender": request.form["birthday"]
                }
                
                if User.validate_patient(patient_data):
                        User.update_patient(patient_data)
                        
                if Patient_Cartel.validate_cartel(data):
                        Patient_Cartel.insert_cartel(data)
                patient = User.get_user_by_id({"id": id})
                cartels = Patient_Cartel.get_cartel_by_id({"patient_id": id})
                return render_template("patient_info.html", patient=patient, cartels=cartels)
        else:
                check_doctor(session)
                patient = User.get_user_by_id({"id": id})
                cartels = Patient_Cartel.get_cartel_by_id({"patient_id": id})
                return render_template("patient_info.html", patient=patient, cartels=cartels)
                


# open colleague page
@app.route("/colleague")
def colleague():
        check_doctor(session)
        
        doctors = User.get_all_doctors() 
        pharmacists = User.get_all_pharmacists()
        nurses = User.get_all_nurses()
        
        return render_template("colleague.html", doctors=doctors, pharmacists=pharmacists, nurses=nurses)

