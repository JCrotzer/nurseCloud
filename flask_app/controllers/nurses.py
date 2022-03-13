from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.nurse import Nurse

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/')
def index():
    return render_template("/index.html")

@app.route('/nurses/register')
def register():
    return render_template("nurse_signup.html")

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
    session["nurse_id"] = Nurse.create_nurse(data)
    return redirect('/nurses/skills')

# READ
@app.route('/nurses/skills')
def nurse_skills():
    if "nurse_id" not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": session['nurse_id']
    }
    this_nurse = Nurse.read_by_id(data)
    return render_template('certs_skills.html', nurse = this_nurse)