import datetime
import os
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.news import News
from flask_app.models.user import User
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'flask_app/static/index/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#add news
@app.route("/news/new", methods=["POST"])
def add_news():
    if "user_id" not in session:
        return redirect("/check")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "link": request.form["link"],
    }

    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["image"] = current_time + filename
            
            News.add_news(data)
            
            return redirect(request.referrer)
    return redirect(request.referrer)


#delete news
@app.route("/deletenews/<int:id>")
def delete_news(id):
    if "user_id" not in session:
        return redirect("/check")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    data = {
        "id": id
    }
    News.delete_news(data)
    return redirect(request.referrer)   

#edit news
@app.route("/viewnews/<int:id>")
def edit_news(id):
    if "user_id" not in session:
        return redirect("/check")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    news = News.get_news_by_id({"id": id})
    return render_template("viewnews.html", news=news)

#edit news
@app.route("/editnews/<int:id>")
def update_news(id):
    if "user_id" not in session:
        return redirect("/check")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    news = News.get_news_by_id({"id": id})
    return render_template("editnews.html", news=news)

#post edit news
@app.route("/posteditnews/<int:id>", methods=["POST"])
def post_edit_news(id):
    if "user_id" not in session:
        return redirect("/check")
    user = User.get_user_by_id({"id": session['user_id']})
    if user['role'] != "A555":
        return redirect("/")
    data = {
        "id": id,
        "title": request.form["title"],
        "description": request.form["description"],
        "link": request.form["link"],
    }
    News.update_news(data)
    return redirect("/shownews")