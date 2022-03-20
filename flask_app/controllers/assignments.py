from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.nurse import Nurse
from flask_app.models.facility import Facility
from flask_app.models.assignment import Assignment

# CREATE

@app.route("/assignments/create", methods=['POST'])
def create_assignment():
    if not Assignment.validate_assignment(request.form):
        return redirect('/assignments/new')
    data = {
        "hospital": request.form['hospital'],
        "speciality": request.form['speciality'],
        "state": request.form['state'],
        "certifications": request.form['certifications'],
        "skills": request.form['skills'],
        "hours": request.form['hours'],
        "shift": request.form['shift'],
        "weeks": request.form['weeks'],
        "starting_date": request.form['starting_date'],
        "phone_number": request.form['phone_number'],
        "facility_id": session['facility_id'],
        }
    Assignment.create_assignment(data)
    return redirect('/facility/dashboard')

# READ

@app.route('/assignments/new')
def add_assignment():
    data = {
        "id": session['facility_id']
    }
    this_facility = Facility.read_by_id(data)
    return render_template("add_assignment.html", facility=this_facility)

@app.route('/assignment/<int:id>')
def display_assignment(id):
    this_assignment = Assignment.read_by_id({"id": id})
    return render_template("dashboard.html", assignment = this_assignment)

@app.route('/job/dashboard')
def job_dashboard():
    return render_template('dashboard.html')

@app.route('/er/jobs')
def er_jobs():
    all_assignments=Assignment.read_all_assignments()
    return render_template('ER_jobs.html', all_assignments=all_assignments)

@app.route('/icu/jobs')
def icu_jobs():
    all_assignments=Assignment.read_all_assignments()
    return render_template('ICU_jobs.html', all_assignments=all_assignments)

@app.route('/med_surg/jobs')
def med_surg_jobs():
    all_assignments=Assignment.read_all_assignments()
    return render_template('medsurg_jobs.html', all_assignments=all_assignments)



# UPDATE

@app.route('/assignments/edit/<int:id>')
def edit_assignment(id):
    data = {
        "id": session['facility_id'],
    }
    assignment_to_edit = Assignment.read_by_id({"id": id})
    return render_template("edit_assignment.html", assignment = assignment_to_edit)

@app.route('/assignments/update', methods=['POST'])
def update_assignment():
    if not Assignment.validate_assignment(request.form):
        return redirect(f"/assignments/edit/{request.form['id']}")
    Assignment.update_assignment(request.form)
    return redirect('/facility/dashboard')

# DELETE

@app.route('/assignments/delete/<int:id>')
def delete_assignment(id):
    Assignment.delete_assignment({"id": id})
    return redirect('/facility/dashboard')