from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.nurse import Nurse
from flask_app.models.facility import Facility

class Assignment:
    db= "nursescloud"
    def __init__(self,data):
        self.id = data['id']
        self.hospital = data['hospital']
        self.speciality = data['speciality']
        self.state = data['state']
        self.certifications = data['certifications']
        self.skills = data['skills']
        self.hours = data['hours']
        self.shift = data['shift']
        self.weeks = data['weeks']
        self.starting_date = data['starting_date']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.nurse = []
        self.facility = []
        
# CREATE

    @classmethod
    def create_assignment(cls, data):
        query = """INSERT INTO assignments (hospital, speciality, state, certifications, skills, hours, shift, weeks, starting_date, phone_number, facility_id)
        VALUES (%(hospital)s, %(speciality)s, %(state)s, %(certifications)s, %(skills)s, %(hours)s, %(shift)s, %(weeks)s, %(starting_date)s, %(phone_number)s, %(facility_id)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# READ

    @classmethod 
    def read_all_assignments(cls):
        query = """
        SELECT * FROM assignments JOIN facilities ON assignments.facility_id = facilities.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_assignments = []
        for row in results:
            this_assignment = cls(row)
            facility_data = {
                "id": row['facilities.id'],
                "name": row['name'],
                "email": row['email'],
                "password" : row['password'],
                "created_at": row['facilities.created_at'],
                "updated_at": row['facilities.updated_at']
            }
            this_facility = Facility(facility_data)
            this_assignment.facility.append(this_facility)
            all_assignments.append(this_assignment)
        return all_assignments

    @classmethod
    def read_by_id(cls, data):
        query = """
        SELECT * FROM assignments JOIN facilities on assignments.facility_id = facilities.id WHERE assignments.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        row = results[0]
        facility_data = {
            "id": session['facility_id'],
            "name": row['name'],
            "email": row['email'],
            "password" : row['password'],
            "created_at": row['facilities.created_at'],
            "updated_at": row['facilities.updated_at']
        }
        this_facility = Facility(facility_data)
        row['facility'] = this_facility
        return cls(row)

# UPDATE

    @classmethod
    def update_assignment(cls, data):
        query="""
        UPDATE assignments
        SET hospital = %(hospital)s, speciality = %(speciality)s, state = %(state)s, certifications = %(certifications)s, skills = %(skills)s,
        hours = %(hours)s, shift = %(shift)s, weeks = %(weeks)s, starting_date = %(starting_date)s, phone_number = %(phone_number)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


# DELETE

    @classmethod
    def delete_assignment(cls, data):
        query = """
        DELETE FROM assignments
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# Validate

    @staticmethod
    def validate_assignment(assignment):
        is_valid = True
        if len(assignment['hospital']) < 3:
            flash("Hospital must be at least 2 characters")
            is_valid = False
        if len(assignment['speciality']) < 2:
            flash("Speciality must be at least 2 characters")
            is_valid = False
        if len(assignment['state']) < 2:
            flash("State must be at least 2 characters")
            is_valid = False
        if len(assignment['hours']) < 2:
            flash("Hours must be at least 2 characters")
            is_valid = False
        if len(assignment['shift']) < 2:
            flash("Shift must be at least 2 characters")
            is_valid = False
        if len(assignment['weeks']) < 1:
            flash("Weeks must be at least 1 character")
            is_valid = False
        if len(assignment['starting_date']) == "":
            flash("Please enter a starting date")
            is_valid = False
        if len(assignment['phone_number']) < 10:
            flash("Phone number must be at least 10 characters")
            is_valid = False
        return is_valid

