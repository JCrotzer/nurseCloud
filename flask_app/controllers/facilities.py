from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.facility import Facility

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route("/facility/register", methods=['POST'])
def register_facility():
    if not Facility.validate(request.form):
        return redirect('/')
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    session["facility_id"] = Facility.register_facility(data)
    return redirect('/dashboard')

# READ

@app.route("/facility/register")
def facility_signup():
    return render_template('facility_signup.html')