import os

from dotenv import load_dotenv

from flask_app.config.mysqlconnection import connectToMySQL

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class ForgotPassword:
    db_name = DB_NAME

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.confirm_code = data['confirm_code']

    @classmethod
    def create_forgot_password(cls, data):
        query = "INSERT INTO forgot_passwords (email, confirm_code,username) VALUES (%(email)s, %(confirm_code)s, %(username)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_last_forgot_password_by_username(cls, data):
        query = "SELECT * FROM forgot_passwords WHERE username = %(username)s ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return results[0]
