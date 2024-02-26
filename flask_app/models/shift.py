from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Shift:
    db_name = "hospital_db"
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.time = data['time']
        self.user_id = data['user_id']
        
    @classmethod
    def get_shift_by_user_id(cls, data):
        query = "SELECT * FROM shifts WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def create_shift(cls, data):
        query = "INSERT INTO shifts (start, end, user_id) VALUES (%(start)s, %(end)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    