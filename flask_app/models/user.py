from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import training
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "fitness"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email  = data['email']
        self.password  = data['password']
        self.created_at  = data['created_at']
        self.updated_at  = data['updated_at']
        self.training = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row) )
        return users

    @classmethod
    def get_all_except_current(cls, current_user_id):
        query = """
        SELECT * FROM user u
        WHERE u.id != %(current_user_id)s
        AND u.id NOT IN(
            SELECT receiver_id FROM friend_requests WHERE sender_id = %(current_user_id)s
            UNION
            SELECT sender_id FROM friend_requests WHERE receiver_id = %(current_user_id)s
        )
        """

        results = connectToMySQL(cls.db).query_db(query, {'current_user_id': current_user_id})
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "Select * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            is_valid= False
        return is_valid