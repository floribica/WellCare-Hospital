import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY
