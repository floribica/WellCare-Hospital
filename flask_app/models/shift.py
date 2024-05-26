import os
from datetime import datetime

from dotenv import load_dotenv
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class Shift:
    db_name = DB_NAME

    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.time = data['time']
        self.user_id = data['user_id']

    # get all shifts
    @classmethod
    def get_shift_by_user_id(cls, data):
        query = "SELECT * FROM shifts WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        shifts = []
        for shift in results:
            shifts.append(shift)
        return shifts

    # get shift by id
    @classmethod
    def get_shift_by_id(cls, data):
        query = "SELECT * FROM shifts WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    # add all shifts
    @classmethod
    def create_shift(cls, data):
        query = ("INSERT INTO shifts (start, end, user_id) "
                 "VALUES (%(start)s, %(end)s, %(user_id)s);")
        return connectToMySQL(cls.db_name).query_db(query, data)

    # confirm shift
    @classmethod
    def confirm_shift(cls, data):
        query = "UPDATE shifts SET done = 1 WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_shift(data):
        is_valid = True
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        end_time = data["end"]

        if data['done'] == 1:
            flash("Shift already confirmed", "shift")
            is_valid = False
        if data["date"] != current_date:
            flash("Shift date is not today", "shift")
            is_valid = False
        end_datetime = datetime.combine(current_date, datetime.min.time()) + end_time
        if end_datetime.time() > current_time:
            flash("Shift does not end yet", "shift")
            is_valid = False

        return is_valid
