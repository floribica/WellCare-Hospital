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
from werkzeug.security import check_password_hash
import bcrypt
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'flask_app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return redirect("/")
    
    doctor = User.get_total_nr_of_doctors()
    patient = User.get_total_nr_of_patients()
    news = News.get_all_news()
    return render_template("index.html" , doctor=doctor, patient=patient , news=news)


@app.route("/check")
def check():
    if "user_id" in session:
        return redirect("/")
    return redirect("/dashboard")

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/check")
    print(session)
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user:
        if user['role'] == "A555":
            return redirect("/admin")
        elif user['role'] == "P493":
            return redirect("/patient")
        elif user['role'] == "D435":
            return redirect("/doctor")
        elif user['role'] == "N792":
            return redirect("/nurse")
        elif user['role'] == "PH528":
            return redirect("/pharmacist")
    
@app.route("/login")
def login():
    if "user_id" in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/login/process", methods=["POST"])
def login_process():
    if "user_id" in session:
        return redirect("/")
    data = {
        "username": request.form["username"]
    }
    user = User.get_user_by_username(data)
    if not user:
        flash("User doesn't exist", "userlogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Password is incorrect", "passlogin")
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/check")


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

#if a route is not found, it will redirect to the login page
@app.errorhandler(404)
def page_not_found(e):
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['role'] == "D435":
        return render_template('404_doctor.html')
    elif user['role'] == "N792":
        return render_template('404_nurse.html')
    elif user['role'] == "P493":
        return render_template('404_patient.html')
    elif user['role'] == "PH528":
        return render_template('404_pharmacist.html')
    elif user['role'] == "A555":
        return render_template('404.html')
    return render_template('/')
    
    
@app.route("/add/photo", methods=["POST"])
def add_photo():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["image"] = current_time + filename
        
    User.add_profil_pic(data)
    return redirect(request.referrer)



@app.route("/profile/<int:id>")
def showProfile(id):
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": id
    }
    user=User.get_user_by_id(data)
    return render_template("showprofile.html", user=user)

@app.route("/reset/<int:id>")
def reset(id):
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": id
    }
    user=User.get_user_by_id(data)
    return render_template("reset.html", user=user)

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

    
    
