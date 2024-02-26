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
    