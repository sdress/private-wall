from flask_app.config.mysqlconnection import connectToMySQL
import math
from datetime import datetime
# if many to many or one to many relationship, may need to import other model

# insert name of schema
db = 'private_wall_schema'

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver_id = data['receiver_id']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    # create method
    @classmethod
    def create(cls, data):
        # some query
        query = "INSERT INTO messages (content, sender_id, receiver_id, created_at, updated_at) VALUES ( %(content)s, %(sender_id)s, %(receiver_id)s, NOW(), NOW() );"
        return connectToMySQL(db).query_db(query, data)
    
    # read
    @classmethod
    def get_all(cls):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id"
        results = connectToMySQL(db).query_db(query)
        all_list = []
        for row in results:
            all_list.append( cls(row) )
            # print(cls(row))
        return all_list
    
    @classmethod
    def get_user_msgs(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE receiver_id =  %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        # print(results)
        if results == False:
            return None
        user_msgs = []
        for row in results:
            user_msgs.append( cls(row) )
        return user_msgs
    
    @classmethod
    def get_sent_msgs(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE sender_id =  %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if results == False:
            return None
        sent_msgs = []
        for row in results:
            sent_msgs.append( row )
        return sent_msgs

    @classmethod
    def delete_msg(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)