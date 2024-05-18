import math
import random
import smtplib
import os

from flask import render_template, request, session, redirect
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

from flask_app import app
from flask_app.models.application import Application
from flask_app.models.forgot_password import ForgotPassword
from flask_app.models.news import News
from flask_app.models.user import User
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
COMPANY_NAME = os.getenv("COMPANY_NAME")


# open admin page
@app.route("/admin")
def admin():
        check = check_admin(session)
        if check:
                return check
        user = User.get_user_by_id({"id": session['user_id']})
        all_users = User.get_all_users()
        applications = Application.get_all_applications()
        applications_count = Application.get_applications_count()
        
        return render_template("admin.html", user=user, all_users=all_users, applications=applications, applications_count=applications_count)  


# open table page for admin
@app.route("/admin/table")
def table():
        check = check_admin(session)
        if check:
                return check
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
        check = check_admin(session)
        if check:
                return check
        return render_template("register.html")


# register new user automatically
@app.route("/register/<int:id>")
def register_auto(id):
        check = check_admin(session)
        if check:
                return check
        app_user = Application.get_application_by_id({"id": id})
        all_users = User.get_all_users()
        return render_template("registerAuto.html", app_user=app_user, all_users=all_users)
        

# create new user account and send email
@app.route("/register/process", methods=["POST"])
def register_process():
        check = check_admin(session)
        if check:
                return check
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

        string = "0123456789ABCDEFGHIJKELNOPKQSTUVYZWXZabcdefhijklmnopqrstuvwxz!@?"
        vCode = ""
        length = len(string)
        
        for i in range(10) :
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
        TOADDRS = request.form['email']
        SENDER = f"{COMPANY_NAME} <{ADMINEMAIL}>"
        SUBJECT = "Your username and password"
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\nContent-Type: text/html\r\n\r\n" % (SENDER, "".join(TOADDRS), SUBJECT))

        msg += f"""
        <html>
        <head>
                <style>
                        body {{
                                font-family: Arial, sans-serif;
                                color: #333;
                                line-height: 1.6;
                        }}
                        .container {{
                                padding: 20px;
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                background-color: #f5f5f5;
                                width: 80%;
                                margin: auto;
                        }}
                        .header {{
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px;
                                text-align: center;
                                border-radius: 8px 8px 0 0;
                        }}
                        .content {{
                                padding: 20px;
                        }}
                        table {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 20px;
                        }}
                        td {{
                                padding: 10px;
                                border: 1px solid #ddd;
                        }}
                        .highlight {{
                                background-color: #f9f9f9;
                        }}
                        .warning {{
                                color: #d9534f;
                        }}
                        .footer {{
                                margin-top: 20px;
                                font-size: 0.9em;
                                color: #777;
                        }}
                </style>
        </head>
        <body>
                <div class="container">
                        <div class="header">
                                <h1>Welcome to WellCare Hospital</h1>
                        </div>
                        <div class="content">
                                <p>Hello <strong>{request.form['fullName']}</strong>,</p>
                                <p>Please use the following information to log in to your account:</p>
                                <table>
                                        <tr class="highlight">
                                                <td><strong>Username:</strong></td>
                                                <td>{request.form['username']}</td>
                                        </tr>
                                        <tr>
                                                <td><strong>Password:</strong></td>
                                                <td>{password}</td>
                                        </tr>
                                </table>
                                <p class="warning">Please change your password after you log in.</p>
                                <p>Best regards,</p>
                                <p><em>WellCare Hospital</em></p>
                        </div>
                        <div class="footer">
                        <p>This email was sent automatically. Please do not reply.</p>
                        </div>
                </div>
        </body>
        </html>
        """

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()

        return redirect("/")


# Forgot password
@app.route("/forgotPassword")
def forgotPassword():
        return render_template("forgotPassword.html")


# Forgot password process
@app.route("/forgotPassword/process", methods=["POST"])
def forgotPassword_process():
        email = request.form["email"]
        user = User.get_user_by_email({"email": email})
        if not user:
                return redirect(request.referrer)
        breakpoint()
        string = "0123456789ABCDEFGHIJKELNOPKQSTUVYZWXZabcdefhijklmnopqrstuvwxz!@?"
        vCode = ""
        length = len(string)
        
        for i in range(6) :
                vCode += string[math.floor(random.random() * length)]
        confirm_code = vCode
        
        data = {
                "email": email,
                "confirm_code": bcrypt.generate_password_hash(confirm_code)
        }
        
        ForgotPassword.create_forgot_password(data)
        
        # send email
        LOGIN = ADMINEMAIL
        TOADDRS = email
        SENDER = f"{COMPANY_NAME} <{ADMINEMAIL}>"
        SUBJECT = "Confirmation code for password reset"
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\nContent-Type: text/html\r\n\r\n" % (SENDER, "".join(TOADDRS), SUBJECT))
        
        msg += f"""
        <html>
        <head>
                <style>
                        body {{
                                font-family: Arial, sans-serif;
                                color: #333;
                                line-height: 1.6;
                        }}
                        .container {{
                                padding: 20px;
                                border: 1px solid
                                #ddd;
                                border-radius: 8px;
                                background-color: #f5f5f5;
                                width: 80%;
                                margin: auto;
                        }}
                        .header {{
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px;
                                text-align: center;
                                border-radius: 8px 8px 0 0;
                        }}
                        .content {{
                                padding: 20px;
                        }}
                        table {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 20px;
                        }}
                        td {{
                                padding: 10px;
                                border: 1px solid
                                #ddd;
                        }}
                        .highlight {{
                                background-color: #f9f9f9;
                        }}
                        .warning {{
                                color: #d9534f;
                        }}
                        .footer {{
                                margin-top: 20px;
                                font-size: 0.9em;
                                color: #777;
                        }}
                </style>
        </head>
        <body>
                <div class="container">
                        <div class="header">
                                <h1>Welcome to WellCare Hospital</h1>
                        </div>
                        <div class="content">
                                <p>Hello,</p>
                                <p>Your confirmation code for password reset is:</p>
                                <table>
                                        <tr class="highlight">
                                                <td><strong>Confirmation Code:</strong></td>
                                                <td>{confirm_code}</td>
                                        </tr>
                                </table>
                                <p class="warning">Please do not share this code with anyone.</p>
                                <p>Best regards,</p>
                                <p><em>WellCare Hospital</em></p>
                        </div>
                        <div class="footer">
                                <p>This email was sent automatically. Please do not reply.</p>
                        </div>
                </div>
        </body>
        </html>
        """
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()
        
        forgot_password = ForgotPassword.get_last_forgot_password_by_email({"email": email})
        if not forgot_password:
                return redirect(request.referrer)
        return render_template("confirmCode.html", forgot_password=forgot_password)


# confirm code
@app.route("/confirmCode/process", methods=["POST"])
def confirmCode_process():
        email = request.form["email"]
        confirm_code = request.form["confirm_code"]
        forgot_password = ForgotPassword.get_last_forgot_password_by_email({"email": email})
        if not forgot_password:
                return redirect(request.referrer)
        
        if not bcrypt.check_password_hash(forgot_password.confirm_code, confirm_code):
                return redirect(request.referrer)
        
        # ganerate new password and send email
        string = "0123456789ABCDEFGHIJKELNOPKQSTUVYZWXZabcdefhijklmnopqrstuvwxz!@?"
        vCode = ""
        length = len(string)
        
        for i in range(10) :
                vCode += string[math.floor(random.random() * length)]
        password = vCode
        
        data = {
                "email": email,
                "password": bcrypt.generate_password_hash(password)
        }
        
        User.edit_password(data)
        
        # send email
        LOGIN = ADMINEMAIL
        TOADDRS = email
        SENDER = f"{COMPANY_NAME} <{ADMINEMAIL}>"
        SUBJECT = "Your new password"
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\nContent-Type: text/html\r\n\r\n" % (SENDER, "".join(TOADDRS), SUBJECT))
        
        msg += f"""
        <html>
        <head>
                <style>
                        body {{
                                font-family: Arial, sans-serif;
                                color: #333;
                                line-height: 1.6;
                        }}
                        .container {{
                                padding: 20px;
                                border: 1px solid
                                #ddd;
                                border-radius: 8px;
                                background-color: #f5f5f5;
                                width: 80%;
                                margin: auto;
                        }}
                        .header {{
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px;
                                text-align: center;
                                border-radius: 8px 8px 0 0;
                        }}
                        .content {{
                                padding: 20px;
                        }}
                        table {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 20px;
                        }}
                        td {{
                                padding: 10px;
                                border: 1px solid
                                #ddd;
                        }}
                        .highlight {{
                                background-color: #f9f9f9;
                        }}
                        .warning {{
                                color: #d9534f;
                        }}
                        .footer {{
                                margin-top: 20px;
                                font-size: 0.9em;
                                color: #777;
                        }}
                </style>
        </head>
        <body>
                <div class="container">
                        <div class="header">
                                <h1>Welcome to WellCare Hospital</h1>
                        </div>
                        <div class="content">
                                <p>Hello,</p>
                                <p>Your new password is:</p>
                                <table>
                                        <tr class="highlight">
                                                <td><strong>Password:</strong></td>
                                                <td>{password}</td>
                                        </tr>
                                </table>
                                <p class="warning">Please change your password after you log in.</p>
                                <p>Best regards,</p>
                                <p><em>WellCare Hospital</em></p>
                        </div>
                        <div class="footer">
                                <p>This email was sent automatically. Please do not reply.</p>
                        </div>
                </div>
        </body>
        </html>
        """
        
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
        check = check_admin(session)
        if check:
                return check
        user = User.get_user_by_id({"id": id})
        return render_template("view.html", user=user)


# edit user info
@app.route("/edit/<int:id>")
def edit(id):
        check = check_admin(session)
        if check:
                return check
        user = User.get_user_by_id({"id": id})
        return render_template("edit.html", user=user)


# edit user info process
@app.route("/edit/process/<int:id>", methods=["POST"])
def edit_process(id):
        check = check_admin(session)
        if check:
                return check
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
        check = check_admin(session)
        if check:
                return check
        User.delete_user({"id": id})
        return redirect("/")


# show all news
@app.route("/shownews")
def shownews():
        check = check_admin(session)
        if check:
                return check
        user = User.get_user_by_id({"id": session['user_id']})
        news = News.get_all_news()
        applications_count = Application.get_applications_count()
        
        return render_template("shownews.html", user=user, news=news, applications_count=applications_count)
