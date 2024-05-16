import os

from flask import render_template, request, session, redirect, flash , url_for
import paypalrestsdk
from dotenv import load_dotenv

from flask_app import app
from flask_app.models.user import User
from flask_app.models.news import News
from flask_app.models.appointment import Appointment
from flask_app.models.testimonial import Testimonial
from flask_app.models.package import Package
from flask_app.controllers.check_user import check_patient


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
        
        return render_template("patient.html", user=user, doctors=doctors,all_doctors=all_doctors , news=news, testimonials=testimonials , packages=packages, contents=contents)


# open page for patient to buy medicine
@app.route("/buy/medicine")
def buy_medicine():
        check = check_patient(session)
        if check:
                return check
        user = User.get_user_by_id({"id": session["user_id"]})
        return render_template("buy.html", user=user)


# open page for patient to find doctor
@app.route("/finddoctor", methods = ['GET','POST'])
def finddoctor():
        check = check_patient(session)
        if check:
                return check
        user = User.get_user_by_id({"id": session["user_id"]})
        if request.method == 'GET':
                doctors = User.get_doctor()
                return render_template("search.html" , user=user, doctors=doctors)
        
        if request.method == 'POST':
                if not request.form['position'] or request.form['position'] == 'all':
                        position = 'all'
                else:
                        position = request.form['position']
                if not request.form['fullName']:
                        fullName = 'all'
                else:
                        fullName = request.form['fullName']+ '%'
                        
                if fullName == 'all' and position =='all':
                        doctors = User.get_doctor()
                elif fullName =='all' and position != 'all':
                        doctors = User.get_doctor_by_position({'position': position})
                elif fullName !='all' and position == 'all':
                        doctors = User.get_doctor_by_fullName({'fullName': fullName})
                elif fullName !='all' and position != 'all':
                        data = {
                            'position' : position,
                            'fullName' : fullName
                        }
                        doctors = User.get_doctor_by_fullName_and_position(data)
                
                return render_template("search.html" , user=user, doctors=doctors)


# create new appointment
@app.route("/appointment/new", methods=["POST"])
def new_appointment():
        check = check_patient(session)
        if check:
                return check
        data = {
            "department": request.form["department"],
            "doctor": request.form["doctor"],
            "fullName": request.form["fullName"],
            "email": request.form["email"],
            "user_id": session["user_id"]
        }
        
        if not Appointment.validate_appointment(data):
                return redirect("/")
    
        if not Appointment.check_appointment(data):
                flash("You already have an appointment with this doctor", "appointmenterror")
                return redirect(request.referrer) 
        
        Appointment.create_appointment(data)
        flash("Appointment created successfully", "success")
        return redirect(request.referrer)


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
                        "mode": "sandbox", # Change this to "live" when you're ready to go live
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
                    "mode": "sandbox", # Change this to "live" when you're ready to go live
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
                        
                        return redirect('/')
                    
                else:
                    flash('Something went wrong with your payment', 'paymentNotSuccessful')
                    return redirect('/')
                
                
        except paypalrestsdk.ResourceNotFound as e:
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
