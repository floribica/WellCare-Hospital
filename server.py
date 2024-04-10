from flask_app import app
from flask_app.controllers import users,admin,doctors,nurses,shifts,patients,applications,testimonials,news
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(debug=True,host=HOST, port=PORT)
