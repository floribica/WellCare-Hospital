import logging
import os
from datetime import datetime

import paypalrestsdk
from dotenv import load_dotenv
from flask import render_template, request, session, redirect, flash, url_for

from flask_app import app
from flask_app.controllers.check_user import check_patient
from flask_app.helpers.send_email import package_email_html, send_email
from flask_app.models.appointment import Appointment
from flask_app.models.news import News
from flask_app.models.package import Package
from flask_app.models.patient_info import Patient_Cartel
from flask_app.models.testimonial import Testimonial
from flask_app.models.user import User

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET_KEY = os.getenv("CLIENT_SECRET_KEY")


# open the patient page
@app.route("/patient")
def patient():
    check = check_patient(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session["user_id"]})
    doctors = User.get_doctor()
    news = News.get_all_news()
    all_doctors = User.get_all_doctors()
    testimonials = Testimonial.get_all_testimonials()
    packages = Package.get_all_packages()
    contents = Package.get_all_contents()

    return render_template(
        "patient/patient.html",
        user=user,
        doctors=doctors,
        all_doctors=all_doctors,
        news=news,
        testimonials=testimonials,
        packages=packages,
        contents=contents
    )


# open page for patient to buy medicine
@app.route("/buy/medicine")
def buy_medicine():
    check = check_patient(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session["user_id"]})
    return render_template("patient/pharmacy_medicine.html", user=user)


# open page for patient to find doctor
@app.route("/finddoctor", methods=['GET', 'POST'])
def find_doctor():
    check = check_patient(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session["user_id"]})
    if request.method == 'GET':
        doctors = User.get_doctor()
        return render_template("patient/search.html", user=user, doctors=doctors)

    if request.method == 'POST':
        if not request.form['position'] or request.form['position'] == 'all':
            position = 'all'
        else:
            position = request.form['position']
        if not request.form['fullName']:
            fullName = 'all'
        else:
            fullName = request.form['fullName'] + '%'

        if fullName == 'all' and position == 'all':
            doctors = User.get_doctor()
        elif fullName == 'all' and position != 'all':
            doctors = User.get_doctor_by_position({'position': position})
        elif fullName != 'all' and position == 'all':
            doctors = User.get_doctor_by_fullName({'fullName': fullName})
        elif fullName != 'all' and position != 'all':
            data = {
                'position': position,
                'fullName': fullName
            }
            doctors = User.get_doctor_by_fullName_and_position(data)

        return render_template("patient/search.html", user=user, doctors=doctors)


# create new appointment
@app.route("/appointment/new", methods=["POST"])
def new_appointment():
    check = check_patient(session)
    if check:
        return check
    if request.form["appointment_date"] < str(datetime.now().date()):
        flash("You can't make an appointment in the past", "appointment_date")
        return redirect(request.referrer)
    if request.form["appointment_time"] < str(datetime.now().time()):
        flash("You can't make an appointment in the past", "appointment_time")
        return redirect(request.referrer)
    data = {
        "department": request.form["department"],
        "doctor": request.form["doctor"],
        "fullName": request.form["fullName"],
        "email": request.form["email"],
        "user_id": session["user_id"],
        "appointment_date": request.form["appointment_date"],
        "appointment_time": request.form["appointment_time"],
    }

    if not Appointment.validate_appointment(data):
        return redirect("/")

    if not Appointment.check_appointment(data):
        flash("You already have an appointment with this doctor", "appointmenterror")
        return redirect(request.referrer)

    Appointment.create_appointment(data)
    flash("Appointment created successfully", "success")
    return redirect(request.referrer)


@app.route("/patient/cartel_view")
def cartel_view():
    check = check_patient(session)
    if check:
        return check
    packages = Package.get_all_patient_packages({"user_id": session["user_id"]})
    cartels = Patient_Cartel.get_cartel_by_id({"patient_id": session["user_id"]})
    return render_template(
        "patient/cartel_view.html",
        packages=packages,
        cartels=cartels
    )


@app.route("/patient/prescription_view")
def prescription_view():
    check = check_patient(session)
    if check:
        return check
    cartels = Patient_Cartel.get_cartel_by_id({"patient_id": session["user_id"]})
    return render_template("patient/prescription_view.html", cartels=cartels)


@app.route("/patient/appointment_view")
def appointment_view():
    check = check_patient(session)
    if check:
        return check
    appointments = Appointment.get_appointment_by_user_id({"user_id": session["user_id"]})
    return render_template("patient/appointment_view.html", appointments=appointments)


# TODO: refactor this to reuse code
# make payment for package
@app.route('/checkout/paypal/<int:id>')
def checkoutPaypal(id):
    check = check_patient(session)
    if check:
        return check
    package = Package.get_package_by_id({'id': id})
    totalPrice = package['price']

    try:
        paypalrestsdk.configure({
            "mode": "sandbox",  # Change this to "live" when you're ready to go live
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET_KEY
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": totalPrice,
                    "currency": "USD"  # Adjust based on your currency
                },
                "description": "Payment for package"
            }],
            "redirect_urls": {
                "return_url": url_for('paymentSuccess', _external=True, totalPrice=totalPrice, package_id=id),
                "cancel_url": "http://example.com/cancel"
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')

            return redirect(approval_url)

        else:
            flash('Something went wrong with your payment', 'creditCardDetails')
            return redirect(request.referrer)

    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'creditCardDetails')
        return redirect(request.referrer)


# payment success
@app.route("/success", methods=["GET"])
def paymentSuccess():
    check = check_patient(session)
    if check:
        return check

    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')

    try:
        paypalrestsdk.configure({
            "mode": "sandbox",  # Change this to "live" when you're ready to go live
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET_KEY
        })

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            ammount = request.args.get('totalPrice')
            status = 'Paid'
            user_id = session['user_id']

            data = {
                'ammount': ammount,
                'status': status,
                'package_id': request.args.get('package_id'),
                'user_id': user_id
            }

            Package.createPayment(data)
            flash('Your payment was successful!', 'paymentSuccessful')

            # Retrieve user information
            user = User.get_user_by_id({'id': user_id})
            user_email = user['email']

            # Retrieve package information
            package_id = request.args.get('package_id')
            package = Package.get_package_by_id({'id': package_id})
            package_name = package['name']
            package_price = package['price']

            # Retrieve package contents
            package_contents = Package.get_contents_by_package_id({'package_id': package_id})
            contents_list = [content['content'] for content in package_contents]

            message = package_email_html(package_name, package_price, contents_list)

            # Send the email
            send_email(user_email, 'Payment Successful', message)

            return redirect('/')

        else:
            flash('Something went wrong with your payment', 'paymentNotSuccessful')
            return redirect('/')

    except paypalrestsdk.ResourceNotFound as e:
        logging.error(e)
        flash('Something went wrong with your payment', 'paymentNotSuccessful')
        return redirect('/')


# payment cancel
@app.route("/cancel", methods=["GET"])
def paymentCancel():
    check = check_patient(session)
    if check:
        return check

    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/')
