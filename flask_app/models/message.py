from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# if many to many or one to many relationship, may need to import other model

# insert name of schema
db = 'private_wall_schema'

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # create method
    @classmethod
    def create(cls, data):
        # some query
        query = "INSERT INTO messages (content, created_at, updated_at) VALUES ( %(msg)s, NOW(), NOW() );"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def add_msg(cls, data):
        query = "INSERT INTO msgs_to_users (user_id, msg_id) VALUES ( %(user_id)s, %(msg_id)s );"
        return connectToMySQL(db).query_db(query, data)

    # read
    @classmethod
    def get_all(cls):
        query = "SELECT messages.*, users.id, users.first_name FROM messages LEFT JOIN msgs_to_users ON msg_id = messages.id LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        all_list = []
        for row in results:
            all_list.append( row )
        return all_list
    
    @classmethod
    def delete_msg(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)