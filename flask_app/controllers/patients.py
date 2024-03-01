import datetime
from flask_app import app
from flask import render_template, request, session, redirect, flash , url_for
from flask_app.models.user import User
from flask_app.models.news import News
from flask_app.models.appointment import Appointment
from flask_app.models.testimonial import Testimonial
from flask_app.models.package import Package
from flask_app.models.shift import Shift
import paypalrestsdk



@app.route("/patient")
def patient():
    if "user_id" not in session:
        return redirect("/check")

    user = User.get_user_by_id({"id": session["user_id"]})
    if user["role"] != "P493":
        return redirect("/check")
    
    doctors = User.get_doctor()
    news = News.get_all_news()
    all_doctors = User.get_all_doctors()
    testimonials = Testimonial.get_all_testimonials()
    packages = Package.get_all_packages()
    contents = Package.get_all_contents()
    return render_template("patient.html", user=user, doctors=doctors,all_doctors=all_doctors , news=news, testimonials=testimonials , packages=packages, contents=contents)


@app.route("/buy/medicine")
def buy_medicine():
    if "user_id" not in session:
        return redirect("/check")

    user = User.get_user_by_id({"id": session["user_id"]})
    if user["role"] != "P493":
        return redirect("/check")

    return render_template("buy.html", user=user)


@app.route("/finddoctor")
def finddoctor():
    if "user_id" not in session:
        return redirect("/check")

    user = User.get_user_by_id({"id": session["user_id"]})
    if user["role"] != "P493":
        return redirect("/check")
    
    doctors = User.get_doctor()

    return render_template("search.html" , user=user, doctors=doctors)

@app.route("/appointment/new", methods=["POST"])
def new_appointment():
    if "user_id" not in session:
        return redirect("/check")
    
    user = User.get_user_by_id({"id": session["user_id"]})
    if user["role"] != "P493":
        return redirect("/check")
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


@app.route('/checkout/paypal/<int:id>')
def checkoutPaypal(id):
    if 'user_id' not in session:
        return redirect('/')
    
    package = Package.get_package_by_id({'id': id})
    totalPrice = package['price']

    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AeFv6D44WQgU1oKDKnadZ_LhguhRmMuPfTWwkn_m6t55IkCQ8JxBa4iMqqIFhF_H8tC6iKx9UTRHbswc",
            "client_secret": "EH3U8tHlSg65KbnM7wvzzyeeoKxGEcM_0ZJnYjs_WMQCJEo7sV9Y2AMzYPFqlLvMizYsOefykMBXlWkQ"
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
                "description": "Pagese per paketen e zgjedhur"
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






@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AeFv6D44WQgU1oKDKnadZ_LhguhRmMuPfTWwkn_m6t55IkCQ8JxBa4iMqqIFhF_H8tC6iKx9UTRHbswc",
            "client_secret": "EH3U8tHlSg65KbnM7wvzzyeeoKxGEcM_0ZJnYjs_WMQCJEo7sV9Y2AMzYPFqlLvMizYsOefykMBXlWkQ"
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


@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/')