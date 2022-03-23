from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# if many to many or one to many relationship, may need to import other model
from flask_app.models import model_name
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# insert name of schema
db = 'name_of_schema'

class Classname:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # insert other required fields as shown in schema
    
    # CRUD BELOW

    # create method
    @classmethod
    def create(cls, data):
        # some query
        query = "INSERT INTO table_name (name, created_at, updated_at) VALUES ( %(name)s, NOW(), NOW() );"
        return connectToMySQL(db).query_db(query, data)
    
    # read
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM table_name;"
        results = connectToMySQL(db).query_db(query)
        all_list = []
        for row in results:
            all_list.append( cls(row) )
        return all_list
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM table_name WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # update
    @classmethod
    def update(cls, data):
        query = "UPDATE table_name SET name = %(name)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    # delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM table_name WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    #basic validation form
    @staticmethod
    def validate_survey(data):
        is_valid = True # we assume this is true
        query = "SELECT * FROM table_name WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) >= 1:
            flash("ID already exists")
            is_valid = False
        if len(data['name']) < 3:
            flash("Name is a required field.")
            is_valid = False
        return is_valid