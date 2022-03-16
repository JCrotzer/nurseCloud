from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_0]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Nurse:
    db = "nursescloud"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE

    @classmethod
    def create_nurse(cls,data):
        query = """
        INSERT INTO nurses (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        results= connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def login_nurse(cls, data):
        this_nurse = cls.read_by_email(data['email'])
        if this_nurse:
            if bcrypt.check_password_hash(this_nurse.password, data['password']):
                session['first_name'] = this_nurse.first_name
                session['nurse_id'] = this_nurse.id
        return this_nurse


# READ

    @classmethod
    def read_by_email(cls,data):
        query = """
        SELECT * FROM nurses WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def read_by_username(cls, data):
        query = "SELECT * FROM nurses WHERE first_name = %(first_name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        else: 
            return cls(results[0])


    @classmethod
    def read_by_id(cls, data):
        query = """
        SELECT * FROM nurses WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_register(nurse):
        is_valid = True
        query = "SELECT * FROM nurses WHERE email = %(email)s;"
        results = connectToMySQL(Nurse.db).query_db(query,{"email": nurse['email']})
        if len(results) > 0:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(nurse['email']):
            flash("Invalid email!")
            is_valid = False
        if len(nurse['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(nurse['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(nurse['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if nurse['password'] != nurse['confirm']:
            flash("Passwords don't match!")
            is_valid = False
        return is_valid
