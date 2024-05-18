import os
import random
import smtplib

from dotenv import load_dotenv
from flask import render_template, request, session, redirect
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.controllers.check_user import check_admin
from flask_app.models.application import Application
from flask_app.models.forgot_password import ForgotPassword
from flask_app.models.news import News
from flask_app.models.user import User

bcrypt = Bcrypt(app)

load_dotenv()
ADMINEMAIL = os.getenv("ADMINEMAIL")
PASSWORD = os.getenv("PASSWORD")
ROLES = {
    "a": os.getenv("ADMIN_ROLE"),
    "d": os.getenv("DOCTOR_ROLE"),
    "n": os.getenv("NURSE_ROLE"),
    "p": os.getenv("PATIENT_ROLE"),
    "f": os.getenv("PHARMACIST_ROLE")
}
COMPANY_NAME = os.getenv("COMPANY_NAME")


def generate_random_string(length):
    chars = "0123456789ABCDEFGHIJKELNOPKQSTUVYZWXZabcdefhijklmnopqrstuvwxz!@?"
    return ''.join(random.choice(chars) for _ in range(length))


def send_email(to_addr, subject, html_content):
    sender = f"{COMPANY_NAME} <{ADMINEMAIL}>"
    msg = f"From: {sender}\r\nTo: {to_addr}\r\nSubject: {subject}\r\nContent-Type: text/html\r\n\r\n{html_content}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(ADMINEMAIL, PASSWORD)
    server.sendmail(sender, to_addr, msg)
    server.quit()


@app.route("/admin")
def admin():
    check = check_admin(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session['user_id']})
    context = {
        "user": user,
        "all_users": User.get_all_users(),
        "applications": Application.get_all_applications(),
        "applications_count": Application.get_applications_count()
    }
    return render_template("admin.html", **context)


@app.route("/admin/table")
def table():
    check = check_admin(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session['user_id']})
    context = {
        "user": user,
        "admins": User.get_all_admins(),
        "doctors": User.get_all_doctors(),
        "nurses": User.get_all_nurses(),
        "patients": User.get_all_patients(),
        "pharmacists": User.get_all_pharmacists(),
        "news": News.get_all_news(),
        "application": Application.total_applications(),
        "applications_count": Application.get_applications_count()
    }
    return render_template("table.html", **context)


@app.route("/register")
def register():
    check = check_admin(session)
    if check:
        return check
    return render_template("register.html")


@app.route("/register/<int:id>")
def register_auto(id):
    check = check_admin(session)
    if check:
        return check
    context = {
        "app_user": Application.get_application_by_id({"id": id}),
        "all_users": User.get_all_users()
    }
    return render_template("registerAuto.html", **context)


@app.route("/register/process", methods=["POST"])
def register_process():
    check = check_admin(session)
    if check:
        return check
    if not User.validate_user(request.form):
        return redirect(request.referrer)

    role = ROLES.get(request.form['role'])
    password = generate_random_string(10)
    data = {
        "fullName": request.form["fullName"],
        "username": request.form["username"],
        "email": request.form["email"],
        "role": role,
        "password": bcrypt.generate_password_hash(password)
    }
    User.create_user(data)

    msg = f"""
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
    send_email(request.form['email'], "Your username and password", msg)

    return redirect("/")


@app.route("/forgotPassword")
def forgotPassword():
    return render_template("forgotPassword.html")


@app.route("/forgotPassword/process", methods=["POST"])
def forgotPassword_process():
    email = request.form["email"]
    username = request.form["username"]
    data = {
        "email": email,
        "username": username
    }
    user = User.get_user_by_email_and_username(data)
    if not user:
        return redirect(request.referrer)
    confirm_code = generate_random_string(6)
    forgot_password_data = {
        "email": email,
        "username": username,
        "confirm_code": bcrypt.generate_password_hash(confirm_code)
    }
    ForgotPassword.create_forgot_password(forgot_password_data)

    msg = f"""
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
    send_email(email, "Confirmation code for password reset", msg)
    forgot_password = ForgotPassword.get_last_forgot_password_by_username(forgot_password_data)
    if not forgot_password:
        return redirect(request.referrer)
    return render_template("confirmCode.html", forgot_password=forgot_password)


@app.route("/confirmCode_process", methods=["POST"])
def confirmCode_process():
    username = request.form["username"]
    email = request.form["email"]
    confirm_code = request.form["confirm_code"]
    forgot_password = ForgotPassword.get_last_forgot_password_by_username({"username": username})
    if not forgot_password or not bcrypt.check_password_hash(forgot_password["confirm_code"], confirm_code):
        return redirect(request.referrer)
    password = generate_random_string(10)
    data = {
        "username": username,
        "password": bcrypt.generate_password_hash(password)
    }
    User.edit_password(data)

    msg = f"""
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
                            <p>Hello,</p>
                            <p>Your new password is:</p>
                            <table>
                                            <tr>
                                                    <td><strong>Username:</strong></td>
                                                    <td>{username}</td>
                                            </tr>
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
    send_email(email, "Your new password", msg)

    return redirect("/dashboard")


@app.route("/view/<int:id>")
def view(id):
    check = check_admin(session)
    if check:
        return check
    user = User.get_user_by_id({"id": id})
    return render_template("view.html", user=user)


@app.route("/edit/<int:id>")
def edit(id):
    check = check_admin(session)
    if check:
        return check
    user = User.get_user_by_id({"id": id})
    return render_template("edit.html", user=user)


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


@app.route("/delete/<int:id>")
def delete(id):
    check = check_admin(session)
    if check:
        return check
    User.delete_user({"id": id})
    return redirect("/")


@app.route("/shownews")
def shownews():
    check = check_admin(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session['user_id']})
    news = News.get_all_news()
    applications_count = Application.get_applications_count()
    return render_template("shownews.html", user=user, news=news, applications_count=applications_count)
