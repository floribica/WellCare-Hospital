from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.controllers.check_user import check_nurse


@app.route("/nurse")
def nurse():
    
        check_nurse(session)
        
        user=User.get_user_by_id({"id": session['user_id']})
        
        return render_template("nurse.html", user=user)

