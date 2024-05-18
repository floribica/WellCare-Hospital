import os

from dotenv import load_dotenv
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


class User:
    db_name = DB_NAME

    def __init__(self, data):

        self.id = data['id']
        self.fullName = data['fullName']
        self.username = data['username']
        self.email = data['email']
        self.role = data['role']
        self.password = data['password']
        self.birthday = data['birthday']
        self.age = data['age']
        self.degree = data['degree']
        self.tel = data['tel']
        self.city = data['city']
        self.short_info = data['short_info']
        self.image = data['image']
        self.postion = data['postion']
        self.gender = data['gender']

    # get user by id
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # get user by username
    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # create a new user
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (fullName, username, email, role, password) VALUES (%(fullName)s, %(username)s, %(email)s, %(role)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # get all patients
    @classmethod
    def get_all_patients(cls):
        query = "SELECT * FROM users WHERE role = 'P493';"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users

    # get total number of doctors
    @classmethod
    def get_total_nr_of_doctors(cls):
        query = "SELECT COUNT(*) as total FROM users WHERE role = 'D435';"
        results = connectToMySQL(cls.db_name).query_db(query)
        doctor = 0
        if results:
            doctor = results[0]
        return doctor

    # get total number of staff
    @classmethod
    def get_total_nr_of_staff(cls):
        query = "SELECT COUNT(*) AS total FROM users WHERE role != 'P493' AND role != 'A555';"
        results = connectToMySQL(cls.db_name).query_db(query)
        staff = 0
        if results:
            staff = results[0]
        return staff

    # get total number of patients
    @classmethod
    def get_total_nr_of_patients(cls):
        query = "SELECT COUNT(*) as total FROM users WHERE role = 'P493';"
        results = connectToMySQL(cls.db_name).query_db(query)
        patients = 0
        if results:
            patients = results[0]
        return patients

    # get only 4 doctors
    @classmethod
    def get_doctor(cls):
        query = "SELECT * FROM users WHERE role = 'D435' LIMIT 4;"
        results = connectToMySQL(cls.db_name).query_db(query)
        doctors = []
        for doctor in results:
            doctors.append(doctor)
        return doctors

    # get all doctors
    @classmethod
    def get_all_doctors(cls):
        query = "SELECT * FROM users WHERE users.role = 'D435';"
        results = connectToMySQL(cls.db_name).query_db(query)
        doctors = []
        for doctor in results:
            doctors.append(doctor)
        return doctors

    # get all pharmacists
    @classmethod
    def get_all_pharmacists(cls):
        query = "SELECT * FROM users WHERE users.role = 'PH528';"
        results = connectToMySQL(cls.db_name).query_db(query)
        pharmacists = []
        for pharmacist in results:
            pharmacists.append(pharmacist)
        return pharmacists

    # get all nurses
    @classmethod
    def get_all_nurses(cls):
        query = "SELECT * FROM users WHERE users.role = 'N792';"
        results = connectToMySQL(cls.db_name).query_db(query)
        nurses = []
        for nurse in results:
            nurses.append(nurse)
        return nurses

    # get all admins
    @classmethod
    def get_all_admins(cls):
        query = "SELECT * FROM users WHERE users.role = 'A555';"
        results = connectToMySQL(cls.db_name).query_db(query)
        admins = []
        for admin in results:
            admins.append(admin)
        return admins

    # edit user as admin
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET fullName = %(fullName)s, username = %(username)s, email = %(email)s, role = %(role)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # delete user as admin
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # update user details
    @classmethod
    def update_user_info(cls, data):
        query = "UPDATE users SET birthday = %(birthday)s, age = %(age)s, degree = %(degree)s, tel = %(tel)s, city = %(city)s, short_info = %(short_info)s, position = %(position)s, gender = %(gender)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # add users details
    @classmethod
    def create_user_info(cls, data):
        query = "INSERT INTO users (birthday, age, degree, tel, city, short_info, position,gender) VALUES (%(birthday)s, %(age)s, %(degree)s, %(tel)s, %(city)s, %(short_info)s, %(user_id)s, %(position)s ,%(gender)s) WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # add profile picture
    @classmethod
    def add_profil_pic(cls, data):
        query = "UPDATE users SET image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # get all users
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users

    # reset password
    @classmethod
    def reset_my_password(cls, data):
        query = "UPDATE users SET password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # get doctor by position
    @classmethod
    def get_doctor_by_position(cls, data):
        query = "SELECT * FROM users WHERE position = %(position)s and role = 'D435'; "
        doctor = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        if doctor:
            for d in doctor:
                users.append(d)
        return users

    # get doctor by fullName
    @classmethod
    def get_doctor_by_fullName_and_position(cls, data):
        query = "SELECT * FROM users WHERE fullName LIKE %(fullName)s and position = %(position)s and role = 'D435'; "
        doctor = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        if doctor:
            for d in doctor:
                users.append(d)
        return users

    @classmethod
    def get_doctor_by_fullName(cls, data):
        query = "SELECT * FROM users WHERE fullName LIKE %(fullName)s and role = 'D435'; "
        doctor = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        if doctor:
            for d in doctor:
                users.append(d)
        return users

    # get doctor by fullName and position
    @classmethod
    def get_doctor_by_fullName_and_position(cls, data):
        query = "SELECT * FROM users WHERE fullName LIKE  %(fullName)s AND position = %(position)s AND role = 'D435';"
        doctor = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        if doctor:
            for d in doctor:
                users.append(d)
        return users

    @classmethod
    def update_patient(cls, data):
        query = "UPDATE users SET age = %(age)s, gender = %(gender)s WHERE id = %(patient_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def edit_password(cls, data):
        query = "UPDATE users SET password = %(password)s WHERE username = %(username)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # validate user
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['fullName']) < 3:
            flash("Name must be at least 3 characters.", "fullregister")
            is_valid = False
        if len(data['username']) < 3:
            flash("Username must be at least 3 characters.", "usernameregister")
            is_valid = False
        if len(data['email']) < 3:
            flash("Email must be at least 3 characters.", "emailregister")
            is_valid = False
        return is_valid

    @classmethod
    def get_user_by_email_and_username(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s AND username = %(username)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # validate user info
    @staticmethod
    def validate_user_info(data):

        is_valid = True

        if len(data['birthday']) < 3:
            flash("Birthday must be at least 3 characters.", "birthdayregister")
            is_valid = False
        if len(data['age']) < 1:
            flash("Age must be at least 3 characters.", "ageregister")
            is_valid = False
        if len(data['degree']) < 3:
            flash("Degree must be at least 3 characters.", "degreeregister")
            is_valid = False
        if len(data['tel']) < 3:
            flash("Tel must be at least 3 characters.", "telregister")
            is_valid = False
        if len(data['city']) < 3:
            flash("City must be at least 3 characters.", "cityregister")
            is_valid = False
        if len(data['short_info']) < 3:
            flash("Short info must be at least 10 characters.", "shortinforegister")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_password(data):
        is_valid = True
        if len(data['newpass']) < 8:
            flash("Password must be at least 8 characters.", "newpass")
            is_valid = False
        if data['newpass'] != data['confirmpass']:
            flash("Passwords do not match.", "confirmpass")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_patient(data):
        is_valid = True
        if len(data['age']) < 3:
            flash("Age must be at least 3 characters.")
            is_valid = False
        if len(data['gender']) < 3:
            is_valid = False
            flash("Gendre must be at least 3 characters.")
        return is_valid
