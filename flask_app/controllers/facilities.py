from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.facility import Facility
from flask_app.models.nurse import Nurse
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
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session["facility_id"] = Facility.create(data)
    return redirect('/facility/dashboard')

@app.route('/facility/login', methods=['POST'])
def login_facility():
    this_facility = Facility.read_by_email({"email": request.form['email']})
    if not this_facility or not bcrypt.check_password_hash(this_facility.password, request.form['password']):
        flash("Invalid email/password")
        return redirect('/')
    session["facility_id"] = this_facility.id
    return redirect('/facility/dashboard')

# READ

@app.route("/facility/register")
def facility_signup():
    return render_template('facility_signup.html')

@app.route("/facility/login")
def facility_login():
    return render_template('facility_login.html')

@app.route('/facility/dashboard')
def facility_dashboard():
    if "facility_id" not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": session['facility_id']
    }
    this_facility = Facility.read_by_id(data)
    return render_template('dashboard.html', facility = this_facility)

@app.route('/logout')
def logout_facility():
    session.pop("facility_id")
    return redirect('/')