import os

from dotenv import load_dotenv
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class Application:
    db_name = DB_NAME

    def __init__(self, data):

        self.id = data['id']
        self.fullName = data['fullName']
        self.email = data['email']
        self.role = data['role']
        self.checked = data['checked']
        self.created_at = data['created_at']

    # create application
    @classmethod
    def create_application(cls, data):

        query = "INSERT INTO applications (fullName, email, role) VALUES (%(fullName)s, %(email)s, %(role)s);"

        return connectToMySQL(cls.db_name).query_db(query, data)

    # get all applications that are not checked
    @classmethod
    def get_all_applications(cls):

        query = "SELECT * FROM applications WHERE checked = 0;"

        results = connectToMySQL(cls.db_name).query_db(query)

        applications = []

        for application in results:
            applications.append(cls(application))

        return applications

    # get all applications
    @classmethod
    def total_applications(cls):

        query = "SELECT * FROM applications;"

        results = connectToMySQL(cls.db_name).query_db(query)

        applications = []

        for application in results:
            applications.append(cls(application))

        return applications

    # get applications count
    @classmethod
    def get_applications_count(cls):

        query = "SELECT COUNT(*) as total FROM applications WHERE checked = 0;"

        results = connectToMySQL(cls.db_name).query_db(query)

        application = 0

        if results:
            application = results[0]

        return application

    # get all applications for email that are checked
    @classmethod
    def get_application_by_email(cls, data):

        query = "SELECT * FROM applications WHERE email = %(email)s and checked = 0;"

        results = connectToMySQL(cls.db_name).query_db(query, data)

        application = None

        if results:
            application = results[0]

        return application

    # update checked
    @classmethod
    def update_checked(cls, data):

        query = "UPDATE applications SET checked = 1 WHERE id = %(id)s;"

        return connectToMySQL(cls.db_name).query_db(query, data)

    # delete application
    @classmethod
    def get_application_by_id(cls, data):

        query = "SELECT * FROM applications WHERE id = %(id)s;"

        results = connectToMySQL(cls.db_name).query_db(query, data)

        application = []

        if results:
            application = results[0]

        return application

    # validate application
    @staticmethod
    def validate_application(data):

        is_valid = True

        if len(data['fullName']) < 3:
            flash("Full name must be at least 3 characters.", "fullNameApp")
            is_valid = False
        if len(data['email']) < 6:
            flash("Email must be at least 6 characters.", "emailApp")
            is_valid = False
        if len(data['role']) < 3:
            flash("Role must be at least 3 characters.", "roleApp")
            is_valid = False

        return is_valid
