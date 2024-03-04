from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class News:
    schema = "hospital_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.link = data['link']
        
    @classmethod
    def get_all_news(cls):
        query = "SELECT * FROM news;"
        results = connectToMySQL(cls.schema).query_db(query)
        news = []
        if results:
            for row in results:
                news.append(row)
            return news
        return news
    
    
    #add news
    @classmethod
    def add_news(cls, data):
        query = "INSERT INTO news (title, description, link, image) VALUES (%(title)s, %(description)s, %(link)s, %(image)s);"
        return connectToMySQL(cls.schema).query_db(query, data)
    
    
    #delete news
    @classmethod
    def delete_news(cls, data):
        query = "DELETE FROM news WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)
    
    #view news
    @classmethod
    def get_news_by_id(cls, data):
        query = "SELECT * FROM news WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if results:
            return results[0]
        return False
    
    
    #edit news
    @classmethod
    def update_news(cls, data):
        query = "UPDATE news SET title = %(title)s, description = %(description)s, link = %(link)s WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)