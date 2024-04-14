import datetime
import os
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.news import News
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import redirect, request, flash
import bcrypt
from dotenv import load_dotenv

bcrypt = Bcrypt(app)

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

ADMIN_ROLE = os.getenv("ADMIN_ROLE")
DOCTOR_ROLE = os.getenv("DOCTOR_ROLE")
NURSE_ROLE = os.getenv("NURSE_ROLE")
PATIENT_ROLE = os.getenv("PATIENT_ROLE")
PHARMACIST_ROLE = os.getenv("PHARMACIST_ROLE")


# open the dashboard page
@app.route("/dashboard")
def dashboard():
    
        if "user_id" in session:
                return redirect("/")
        
        doctor = User.get_total_nr_of_doctors()
        patient = User.get_total_nr_of_patients()
        news = News.get_all_news()
        
        return render_template("index.html" , doctor=doctor, patient=patient , news=news)


# check if I have a user in session and redirect to the correct page
@app.route("/check")
def check():
    
        if "user_id" in session:
                return redirect("/")
            
        return redirect("/dashboard")


# check which role the user has and redirect to the correct page
@app.route("/")
def index():
    
        if "user_id" not in session:
                return redirect("/check")
        
        user=User.get_user_by_id({"id": session["user_id"]})
        
        if user:
                if user['role'] == ADMIN_ROLE:
                        return redirect("/admin")
                elif user['role'] == PATIENT_ROLE:
                        return redirect("/patient")
                elif user['role'] == DOCTOR_ROLE:
                        return redirect("/doctor")
                elif user['role'] == NURSE_ROLE:
                        return redirect("/nurse")
                elif user['role'] == PHARMACIST_ROLE:
                        return redirect("/pharmacist")
        
        session.clear()
        return redirect(request.referrer)


# open login page
@app.route("/login")
def login():
    
        if "user_id" in session:
                return redirect("/")
        
        return render_template("login.html")


# process login
@app.route("/login/process", methods=["POST"])
def login_process():
    
        if "user_id" in session:
                return redirect("/")
            
        user = User.get_user_by_username({"username": request.form["username"]})
        
        if not user:
                flash("User doesn't exist", "userlogin")
                return redirect(request.referrer)
            
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
                flash("Password is incorrect", "passlogin")
                return redirect(request.referrer)
            
        session['user_id'] = user['id']
        
        return redirect("/")


# logout
@app.route("/logout")
def logout():
   
        session.clear()
        
        return redirect("/check")


# add user profile
@app.route("/profile/info", methods=["POST"])
def profile_info():
    
        if "user_id" not in session:
                return redirect("/check")
            
        info = User.get_user_by_id({"id": session['user_id']})
        
        if info:
                return redirect(request.referrer)
            
        data = {
            "birthday": request.form["birthday"],
            "age": request.form["age"],
            "degree": request.form["degree"],
            "tel": request.form["tel"],
            "city": request.form["city"],
            "short_info": request.form["short_info"],
            "user_id": session['user_id'],
            "position": request.form["position"],
            "gender": request.form["gender"]
        }
        
        if not User.validate_user_info(data):
                return redirect(request.referrer)
            
        User.create_user_info(data)
        
        return redirect(request.referrer)


# update user profile
@app.route("/profile/update", methods=["POST"])
def profile_update():
    
        if "user_id" not in session:
                return redirect("/check")
        data = {
            "id": session['user_id'],
            "birthday": request.form["birthday"],
            "age": request.form["age"],
            "degree": request.form["degree"],
            "tel": request.form["tel"],
            "city": request.form["city"],
            "short_info": request.form["short_info"],
            "position": request.form["position"],
            "gender": request.form['gender']
        }
        
        User.update_user_info(data)
        
        return redirect(request.referrer)


# if a route is not found, it will redirect to the login page
@app.errorhandler(404)
def page_not_found(e):
    
        if "user_id" not in session:
                return redirect("/check")
            
        user = User.get_user_by_id({"id": session['user_id']})
        
        if user['role'] == DOCTOR_ROLE:
                return render_template('404_doctor.html')
        elif user['role'] == NURSE_ROLE:
                return render_template('404_nurse.html')
        elif user['role'] == PATIENT_ROLE:
                return render_template('404_patient.html')
        elif user['role'] == PHARMACIST_ROLE:
                return render_template('404_pharmacist.html')
        elif user['role'] == ADMIN_ROLE:
                return render_template('404.html')
            
        return render_template('/')
    

# add profile picture
@app.route("/add/photo", methods=["POST"])
def add_photo():
    
        if "user_id" not in session:
            return redirect("/check")
        
        data = { "id": session['user_id'] }
        
        if 'image' in request.files:
            image = request.files['image']
            
            if image.filename != '':
                
                    # check if the file is allowed by ALLOWED_EXTENSIONS
                    if image and '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                            # add current timi in the file name
                            filename = secure_filename(image.filename)
                            filename = str(datetime.now().timestamp()) + filename
                            image.save(os.path.join(UPLOAD_FOLDER, filename))
                            data['image'] = filename
                    else:
                            flash("File not allowed", "image")
                            return redirect(request.referrer)
            
        User.add_profil_pic(data)   
        
        return redirect(request.referrer)


# show profile of a user
@app.route("/profile/<int:id>")
def showProfile(id):
    
        if "user_id" not in session:
                return redirect("/check")
            
        user=User.get_user_by_id({"id": id})
        
        return render_template("showprofile.html", user=user)


# reset password
@app.route("/reset/<int:id>")
def reset(id):
    
        if "user_id" not in session:
                return redirect("/check")
            
        user=User.get_user_by_id({"id": id})
        
        return render_template("reset.html", user=user)


# process reset password
@app.route("/reset/password", methods=["POST"])
def reset_password():
    
        if "user_id" not in session:
                return redirect("/check")
            
        data = {
            "id": session['user_id'],
            "oldpass": request.form["oldpass"],
            "newpass": request.form["newpass"],
            "confirmpass": request.form["confirmpass"]
        }
        
        user = User.get_user_by_id(data)
        
        if not user:
                flash("User not found", "error")
                return redirect(request.referrer)
        if not bcrypt.check_password_hash(user['password'], data['oldpass']):
                flash("Old password is incorrect", "oldpass")
                return redirect(request.referrer)
        if not User.validate_password(data):
                return redirect(request.referrer)

        data2 = {
            "id": session['user_id'],
            "password": bcrypt.generate_password_hash(request.form['newpass'])
        }
        
        User.reset_my_password(data2)
        
        return redirect("/")

    
    
