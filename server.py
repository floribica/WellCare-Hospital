import os

from dotenv import load_dotenv

from flask_app import app
from flask_app.controllers import (
    users,
    admin,
    doctors,
    nurses,
    patients,
    applications,
    testimonials,
    news,
    check_user
)

load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)
