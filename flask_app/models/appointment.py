from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from dotenv import load_dotenv
import os


load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class Appointment:
        db_name = DB_NAME
        def __init__(self, data):
                self.id = data['id']
                self.department = data['department']
                self.doctor = data['doctor']
                self.fullName = data['fullName']
                self.email = data['email']
                self.checked = data['checked']
            
        
        
        #create a new appointment
        @classmethod
        def create_appointment(cls, data):
            
                query = "INSERT INTO appointments (department, doctor, fullName, email, user_id) VALUES (%(department)s, %(doctor)s, %(fullName)s, %(email)s, %(user_id)s);"
            
                return connectToMySQL(cls.db_name).query_db(query, data)
        
        
        
        #check if the user already has an appointment with this doctor in same date 
        @classmethod
        def check_appointment(cls, data):
           
                query = "SELECT * FROM appointments WHERE user_id = %(user_id)s AND doctor = %(doctor)s;"
            
                results = connectToMySQL(cls.db_name).query_db(query, data)
            
                if results and results[0]['checked'] == 0:
                        return False
                
                return True
        
            
        
        #validate appointment
        @staticmethod
        def validate_appointment(data):
            
                is_valid = True
            
                if len(data['department']) < 1:
                        flash("Department is required", "department")
                        is_valid = False
                if len(data['doctor']) < 1:
                        flash("Doctor is required", "doctor")
                        is_valid = False
                if len(data['fullName']) < 1:
                        flash("Full Name is required", "fullName")
                        is_valid = False
                if len(data['email']) < 8:
                        flash("Email is required", "email")
                        is_valid = False
                        
                return is_valid