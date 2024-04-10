from dotenv import load_dotenv
import os

from flask import redirect

from flask_app.models.user import User

load_dotenv()
ADMINEMAIL = os.getenv("ADMINEMAIL")
PASSWORD = os.getenv("PASSWORD")
ADMIN_ROLE = os.getenv("ADMIN_ROLE")
DOCTOR_ROLE = os.getenv("DOCTOR_ROLE")
NURSE_ROLE = os.getenv("NURSE_ROLE")
PATIENT_ROLE = os.getenv("PATIENT_ROLE")
PHARMACIST_ROLE = os.getenv("PHARMACIST_ROLE")


#check if user is logged in and if user is admin
def check_admin (session):
        if "user_id" not in session:
                return redirect("/check")
        
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] != ADMIN_ROLE:
                return redirect("/")



#check if user is logged in and if user is doctor
def check_doctor (session):
        if "user_id" not in session:
                return redirect("/check")
        
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] != DOCTOR_ROLE:
                return redirect("/")
            


#check if user is logged in and if user is nurse
def check_nurse (session):
        if "user_id" not in session:
                return redirect("/check")
        
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] != NURSE_ROLE:
                return redirect("/")



#check if user is logged in and if user is patient
def check_patient (session):
        if "user_id" not in session:
                return redirect("/check")
        
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] != PATIENT_ROLE:
                return redirect("/")
            
            
            
#check if user is logged in and if user is pharmacist
def check_pharmacist (session):
        if "user_id" not in session:
                return redirect("/check")
        
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] != PHARMACIST_ROLE:
                return redirect("/")
            
            
