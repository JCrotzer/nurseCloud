from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.nurse import Nurse

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/nurses/register', methods=['POST'])
def register_nurse():

    if not Nurse.validate_register(request.form):
        return redirect('/nurses/register')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    this_nurse = Nurse.create_nurse(data)
    print (this_nurse)
    session['nurse_id'] = Nurse.create_nurse(data)
    return redirect('/nurses/skills')

@app.route('/nurses/login', methods=['POST'])
def login_nurse():
    this_nurse = Nurse.read_by_email({"email": request.form['email']})
    if not this_nurse:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(this_nurse.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['nurse_id'] = this_nurse.id
    return redirect('/dashboard')


# READ

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/nurses/register')
def nurse_register():
    return render_template('nurse_signup.html')

@app.route('/nurses/login')
def nurse_login():
    return render_template("nurse_login.html")

@app.route('/nurses/skills')
def certs_skills():
    if "nurse_id" not in session:
        flash("You must be logged in to view this page")
        return redirect('/nurses/skills')
    data = {
        "id": session['nurse_id']
    }
    this_nurse = Nurse.read_by_id(data)
    return render_template('certs_skills.html', nurse = this_nurse)

@app.route('/dashboard')
def dashboard():
    if "nurse_id" not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": session['nurse_id']
    }
    this_nurse = Nurse.read_by_id(data)
    return render_template('dashboard.html', nurse = this_nurse)