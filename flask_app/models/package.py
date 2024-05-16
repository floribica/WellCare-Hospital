import os

from dotenv import load_dotenv

from flask_app.config.mysqlconnection import connectToMySQL


load_dotenv()
DB_NAME = os.getenv("DB_NAME")

class Package:
        db_name = DB_NAME
        def __init__(self, data):
                self.id = data['id']
                self.name = data['name']
                self.price = data['price']
                self.image = data['image']
            
            
        #create payment     
        @classmethod
        def createPayment(cls, data):
                query = "INSERT INTO payments (ammount, status,package_id, user_id) VALUES (%(ammount)s, %(status)s,%(package_id)s ,%(user_id)s);"
                return connectToMySQL(cls.db_name).query_db(query, data)
        
        
        #get all packages and left joing contents
        @classmethod
        def get_all_packages(cls):
                query = "SELECT * FROM packages;"
                results = connectToMySQL(cls.db_name).query_db(query)
            
                packages = []
                for package in results:
                        packages.append(package)
                return packages
        
        
        #get all contetns
        @classmethod
        def get_all_contents(cls):
                query = "SELECT * FROM contents;"
                results = connectToMySQL(cls.db_name).query_db(query)
                contents = []
                for content in results:
                        contents.append(content)
                return contents
        
        
        #get package by id
        @classmethod
        def get_package_by_id(cls, data):
                query = "SELECT * FROM packages WHERE id = %(id)s;"
                results = connectToMySQL(cls.db_name).query_db(query, data)
                if results:
                        return results[0]
                return False