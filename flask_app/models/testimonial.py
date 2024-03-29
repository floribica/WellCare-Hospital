from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Testimonial:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        
        
    #create a new testimonial
    @classmethod
    def create_testimonial(cls, data):
        query = "INSERT INTO testimonials (description, user_id) VALUES (%(description)s, %(user_id)s);"
        return connectToMySQL("hospital_db").query_db(query, data)
    
    #get all testimonials with user info
    @classmethod
    def get_all_testimonials(cls):
        query = "SELECT * FROM testimonials JOIN users ON testimonials.user_id = users.id;"
        results = connectToMySQL("hospital_db").query_db(query)
        testimonials = []
        for testimonial in results:
            testimonials.append(testimonial)
        return testimonials
    
    #validate testimonial
    @staticmethod
    def validate_testimonial(data):
        is_valid = True
        if len(data['description']) < 10:
            flash("Description is required", "testimonialerror")
            is_valid = False
        return is_valid