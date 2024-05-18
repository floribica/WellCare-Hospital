import os
from datetime import datetime

from dotenv import load_dotenv
from flask import render_template, request, session, redirect
from werkzeug.utils import secure_filename

from flask_app import app
from flask_app.controllers.check_user import check_admin
from flask_app.models.news import News

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


# add news
@app.route("/news/new", methods=["POST"])
def add_news():
    check = check_admin(session)
    if check:
        return check
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "link": request.form["link"],
    }

    if 'image' in request.files:
        image = request.files['image']
        if image.filename != "":

            if image:
                # save the image in the upload folder with timestamp in the name
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, str(datetime.now().timestamp()) + filename))
                data["image"] = str(datetime.now().timestamp()) + filename
            # check if the file is an image in the allowed extensions
            if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                News.add_news(data)
                return redirect(request.referrer)
            return redirect(request.referrer)
    return redirect(request.referrer)


# delete news
@app.route("/deletenews/<int:id>")
def delete_news(id):
    check = check_admin(session)
    if check:
        return check
    News.delete_news({"id": id})
    return redirect(request.referrer)


# edit news
@app.route("/viewnews/<int:id>")
def edit_news(id):
    check = check_admin(session)
    if check:
        return check
    news = News.get_news_by_id({"id": id})
    return render_template("news/viewnews.html", news=news)


# edit news
@app.route("/editnews/<int:id>")
def update_news(id):
    check = check_admin(session)
    if check:
        return check
    news = News.get_news_by_id({"id": id})
    return render_template("news/editnews.html", news=news)


# post edit news
@app.route("/posteditnews/<int:id>", methods=["POST"])
def post_edit_news(id):
    check = check_admin(session)
    if check:
        return check
    data = {
        "id": id,
        "title": request.form["title"],
        "description": request.form["description"],
        "link": request.form["link"],
    }
    News.update_news(data)
    return redirect("/shownews")
