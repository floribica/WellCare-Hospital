import os

from flask import flash
from dotenv import load_dotenv

from flask_app.config.mysqlconnection import connectToMySQL


load_dotenv()
DB_NAME = os.getenv("DB_NAME")

class Patient_Cartel:
    db_name = DB_NAME
    def __init__(self, data):
        self.id = data['id']
        self.examinate = data['examinate']
        self.treatment = data['treatment']
        self.medicalReport = data['medicalReport']
        self.summary = data['summary']
        self.writer = data['writer']
        self.patient_id = data['patient_id']
        self.created_at = data['created_at']
        
    @classmethod
    def get_cartel_by_id(cls, data):
        query = "SELECT * FROM patient_cartels WHERE patient_id = %(patient_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        cartels = []
        for cartel in results:
            cartels.append(cls(cartel))
        return cartels


    @classmethod
    def insert_cartel(cls, data):
        query = "INSERT INTO patient_cartels (examinate, treatment, medicalReport, summary, writer, patient_id) VALUES (%(examinate)s, %(treatment)s, %(medicalReport)s, %(summary)s, %(writer)s, %(patient_id)s);"
        return connectToMySQL(DB_NAME).query_db(query, data)


    @staticmethod
    def validate_cartel(data):
        is_valid = True
        if len(data['examinate']) < 3:
            flash("Examinate must be at least 3 characters.", "examinate_error")
            is_valid = False
        if len(data['treatment']) < 3:
            flash("Treatment must be at least 3 characters.", "treatment_error")
            is_valid = False
        if len(data['medicalReport']) < 3:
            flash("Medical Report must be at least 3 characters.", "medicalReport_error")
            is_valid = False
        if len(data['summary']) < 3:
            flash("Summary must be at least 3 characters.", "summary_error")
            is_valid = False
        return is_valid
        