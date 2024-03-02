import datetime
import os
import math
import random
import smtplib
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.application import Application
from flask_app.models.news import News
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
from werkzeug.utils import secure_filename
from datetime import datetime
bcrypt = Bcrypt(app)

from .env import ADMINEMAIL
from .env import PASSWORD

UPLOAD_FOLDER = 'flask_app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user['role'] != "A555":
        return redirect("/")
    
    all_users = User.get_all_users()
    applications = Application.get_all_applications()
    applications_count = Application.get_applications_count()
    return render_template("admin.html", user=user, all_users=all_users, applications=applications, applications_count=applications_count)  


@app.route("/admin/table")
def table():
    if "user_id" not in session:
        return redirect("/check")
    data = {
        "id": session['user_id']
    }
    user=User.get_user_by_id(data)
    if user['role'] != "A555":
        return redirect("/")
    
    admins = User.get_all_admins()
    doctors = User.get_all_doctors()
    nurses = User.get_all_nurses()
    patients = User.get_all_patients()
    pharmacists = User.get_all_pharmacists()
    news = News.get_all_news()
    application = Application.total_applications()
    applications_count = Application.get_applications_count()
    return render_template("table.html",user=user, admins=admins, doctors=doctors, nurses=nurses, patients=patients, pharmacists=pharmacists, news=news, application=application ,applications_count=applications_count)


#register new user manually
@app.route("/register")
def register():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    return render_template("register.html")

#register new user automatically
@app.route("/register/<int:id>")
def register_auto(id):
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    app_user = Application.get_application_by_id({"id": id})
    return render_template("registerAuto.html", app_user=app_user)
    

@app.route("/register/process", methods=["POST"])
def register_process():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    
    if request.form['role'] == "a":
        role = "A555"
    elif request.form['role'] == "d":
        role = "D435"
    elif request.form['role'] == "n":
        role = "N792"
    elif request.form['role'] == "p":
        role = "P493"
    elif request.form['role'] == "f":
        role = "PH528"
    
    string = '0123456789ABCDEFGHIJKELNOPKQSTUV'
    vCode = ""
    length = len(string)
    for i in range(8) :
        vCode += string[math.floor(random.random() * length)]
    password = vCode
    
    data = {
        "fullName": request.form["fullName"],
        "username": request.form["username"],
        "email": request.form["email"],
        "role": role,
        "password": bcrypt.generate_password_hash(password)
    }
    User.create_user(data)
    application = Application.get_application_by_email({"email": request.form["email"]})
    data2 = {
        "id": application['id']
    }
    Application.update_checked(data2)
    
    LOGIN = ADMINEMAIL
    TOADDRS  = request.form['email']
    SENDER = ADMINEMAIL
    SUBJECT = 'This is your password'
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
        % ((SENDER), "".join(TOADDRS), SUBJECT) )
    msg += f'Your username is: {request.form["username"]}\n'
    msg += f'Your password is: {password}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect("/")



