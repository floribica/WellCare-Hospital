from flask import render_template, session

from flask_app import app
from flask_app.controllers.check_user import check_nurse
from flask_app.models.user import User


@app.route("/nurse")
def nurse():
    check = check_nurse(session)
    if check:
        return check
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("nurse.html", user=user)
