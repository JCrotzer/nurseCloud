from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_0]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Facility:
    db = "nursescloud"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.name = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE

    @classmethod
    def create(cls, data):
        query = """INSERT INTO facilities (name, email, password)
        VALUES (%(name)s, %(email)s, %(password)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def login_facility(cls, data):
        this_facility = cls.read_by_email(data['email'])
        if this_facility:
            if bcrypt.check_password_hash(this_facility.password, data['password']):
                session['name'] = this_facility.name
                session['facility_id'] = this_facility.id
        return this_facility

# READ

    @classmethod
    def read_by_email(cls, data):
        query = """
        SELECT * FROM facilities WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def read_by_id(cls, data):
        query = """
        SELECT * FROM facilities WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def read_by_username(cls, data):
        query = "SELECT * FROM facilities WHERE name = %(name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            return cls(results[0])


# VALIDATE

    @staticmethod
    def validate(facility):
        is_valid = True
        query = "SELECT * FROM facilities WHERE email = %(email)s;"
        results = connectToMySQL(Facility.db).query_db(query, {"email": facility['email']})
        if len(results) > 0:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(facility['email']):
            flash("Invalid email!")
            is_valid = False
        if len(facility['name']) < 3:
            flash("Facility name must be at least 3 characters")
            is_valid = False
        if len(facility['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if facility['password'] != facility['confirm']:
            flash("Passwords don't match")
            is_valid = False
        return is_valid