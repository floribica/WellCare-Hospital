import math
import random
import smtplib
from flask_app import app
from flask import render_template, request, session, redirect
from flask_app.models.application import Application
from flask_app.models.news import News
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from flask_app.controllers.check_user import check_admin


bcrypt = Bcrypt(app)

load_dotenv()
ADMINEMAIL = os.getenv("ADMINEMAIL")
PASSWORD = os.getenv("PASSWORD")
ADMIN_ROLE = os.getenv("ADMIN_ROLE")
DOCTOR_ROLE = os.getenv("DOCTOR_ROLE")
NURSE_ROLE = os.getenv("NURSE_ROLE")
PATIENT_ROLE = os.getenv("PATIENT_ROLE")
PHARMACIST_ROLE = os.getenv("PHARMACIST_ROLE")


# open admin page
@app.route("/admin")
def admin():
    
        check_admin(session)

        user = User.get_user_by_id({"id": session['user_id']})
        all_users = User.get_all_users()
        applications = Application.get_all_applications()
        applications_count = Application.get_applications_count()
        
        return render_template("admin.html", user=user, all_users=all_users, applications=applications, applications_count=applications_count)  


# open table page for admin
@app.route("/admin/table")
def table():
    
        check_admin(session)

        user = User.get_user_by_id({"id": session['user_id']})
        admins = User.get_all_admins()
        doctors = User.get_all_doctors()
        nurses = User.get_all_nurses()
        patients = User.get_all_patients()
        pharmacists = User.get_all_pharmacists()
        news = News.get_all_news()
        application = Application.total_applications()
        applications_count = Application.get_applications_count()
        
        return render_template("table.html",user=user, admins=admins, doctors=doctors, nurses=nurses, patients=patients,    pharmacists=pharmacists, news=news, application=application ,applications_count=applications_count)


# register new user manually
@app.route("/register")
def register():
    
        check_admin(session)
            
        return render_template("register.html")


# register new user automatically
@app.route("/register/<int:id>")
def register_auto(id):
    
        check_admin(session)
            
        app_user = Application.get_application_by_id({"id": id})
        all_users = User.get_all_users()
        
        return render_template("registerAuto.html", app_user=app_user, all_users=all_users)
        

# create new user account and send email
@app.route("/register/process", methods=["POST"])
def register_process():
    
        check_admin(session)
        
        if not User.validate_user(request.form):
                return redirect(request.referrer)

        if request.form['role'] == "a":
                role = ADMIN_ROLE
        elif request.form['role'] == "d":
                role = DOCTOR_ROLE
        elif request.form['role'] == "n":
                role = NURSE_ROLE
        elif request.form['role'] == "p":
                role = PATIENT_ROLE
        elif request.form['role'] == "f":
                role = PHARMACIST_ROLE

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

        LOGIN = ADMINEMAIL
        TOADDRS  = request.form['email']
        SENDER = ADMINEMAIL
        SUBJECT = "Your username and password"
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'Hello {request.form["fullName"]},\n'
        msg += f'Please use the following information to log in to your account:\n'
        msg += f'Your username is: {request.form["username"]}\n'
        msg += f'Your password is: {password}'
        msg += f'\n Please change your password after you log in. \n'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()

        return redirect("/")


# view user info
@app.route("/view/<int:id>")
def view(id):
    
        check_admin(session)
        
        user = User.get_user_by_id({"id": id})
        
        return render_template("view.html", user=user)


# edit user info
@app.route("/edit/<int:id>")
def edit(id):
    
        check_admin(session)
        
        user = User.get_user_by_id({"id": id})
        
        return render_template("edit.html", user=user)


# edit user info process
@app.route("/edit/process/<int:id>", methods=["POST"])
def edit_process(id):
    
        check_admin(session)
        
        if not User.validate_user(request.form):
                return redirect(request.referrer)
            
        data = {
                "id": id,
                "fullName": request.form["fullName"],
                "username": request.form["username"],
                "email": request.form["email"],
                "role": request.form["role"],
        }
        
        User.edit_user(data)
        
        return redirect("/")


# delete user
@app.route("/delete/<int:id>")
def delete(id):
    
        check_admin(session)
        
        User.delete_user({"id": id})
        
        return redirect("/")


# show all news
@app.route("/shownews")
def shownews():
    
        check_admin(session)
        
        user = User.get_user_by_id({"id": session['user_id']})
        news = News.get_all_news()
        applications_count = Application.get_applications_count()
        
        return render_template("shownews.html", user=user, news=news, applications_count=applications_count)
