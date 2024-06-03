import os

from dotenv import load_dotenv
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class Nurse_treatments:
    db_name = DB_NAME

    def __init__(self, data):
        self.temperature = data['temperature']
        self.blood_pressure = data['blood_pressure']
        self.heart_rate = data['heart_rate']
        self.respiratory_rate = data['respiratory_rate']
        self.oxygen_saturation = data['oxygen_saturation']
        self.pain_level = data['pain_level']
        self.notes = data['notes']
        self.nurse_id = data['nurse_id']
        self.patient_id = data['patient_id']
        

        
        
    @classmethod
    def get_cartel_by_id(cls, data):
        query = "SELECT nurse_treatments.* ,users.fullName FROM nurse_treatments LEFT JOIN users ON nurse_treatments.nurse_id = users.id WHERE nurse_treatments.patient_id = %(patient_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        cartels = []
        if results:
            for cartel in results:
                cartels.append(cartel)
        return cartels
    
    
    @classmethod
    def add_cartel(cls, data):
        query = ("INSERT INTO nurse_treatments (temperature, blood_pressure, heart_rate, respiratory_rate, oxygen_saturation, pain_level, notes, nurse_id, patient_id) "
                 "VALUES (%(temperature)s, %(blood_pressure)s, %(heart_rate)s, %(respiratory_rate)s, %(oxygen_saturation)s, %(pain_level)s, %(notes)s, %(nurse_id)s, %(patient_id)s);")
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_cartel(data):
        is_valid = True
        if len(data['temperature']) == 0:
            flash("Temperature is required","temperature")
            is_valid = False
        if len(data['blood_pressure']) == 0:
            flash("Blood Pressure is required","blood_pressure")
            is_valid = False
        if len(data['heart_rate']) == 0:
            flash("Heart Rate is required","heart_rate")
            is_valid = False
        if len(data['respiratory_rate']) == 0:
            flash("Respiratory Rate is required","respiratory_rate")
            is_valid = False
        if len(data['oxygen_saturation']) == 0:
            flash("Oxygen Saturation is required","oxygen_saturation")
            is_valid = False
        if len(data['pain_level']) == 0:
            flash("Pain Level is required","pain_level")
            is_valid = False
        if len(data['notes']) == 10:
            flash("Notes is required","notes")
            is_valid = False
        return is_valid
    