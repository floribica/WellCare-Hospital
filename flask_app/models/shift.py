from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from dotenv import load_dotenv
import os


load_dotenv()
DB_NAME = os.getenv("DB_NAME")

class Shift:
    
        db_name = DB_NAME
    
        def __init__(self, data):
                self.id = data['id']
                self.date = data['date']
                self.time = data['time']
                self.user_id = data['user_id']
        
        
        
        #get all shifts
        @classmethod
        def get_shift_by_user_id(cls, data):
            
                query = "SELECT * FROM shifts WHERE user_id = %(id)s;"
            
                results = connectToMySQL(cls.db_name).query_db(query, data)
            
                if results:
                        return results[0]
                
                return False
        
        
        
        #add all shifts
        @classmethod
        def create_shift(cls, data):
            
                query = "INSERT INTO shifts (start, end, user_id) VALUES (%(start)s, %(end)s, %(user_id)s);"
            
                return connectToMySQL(cls.db_name).query_db(query, data)
            