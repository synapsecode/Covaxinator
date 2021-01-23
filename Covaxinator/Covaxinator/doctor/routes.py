from flask import render_template, request, Blueprint, flash, jsonify, url_for, session, redirect
from Covaxinator.models import *
from Covaxinator import db

doctor = Blueprint('doctor', __name__)

@doctor.route('/login', methods=['GET', 'POST'])
def doctor_login():
	if(request.method == 'POST'):
		data = request.form
		phone = data['phone']
		password = data['password']
		doctor = Doctor.query.filter_by(phone=phone).first()
		print("DOC", doctor)
		if(not doctor or doctor.password != password):
			print("INVALID")
			flash('Invalid Credentials!', 'danger')
			return jsonify({"redirect": url_for('doctor.doctor_login')})

		flash('Login Completed Successfully!', 'success')
		session['logged_in_doctor'] = doctor.id
		return jsonify({"redirect": url_for('doctor.doctor_home')})
	return render_template('doctor/login.html', title='Doctor Login')

@doctor.route('/register', methods=['GET', 'POST'])
def doctor_register():
	if(request.method == 'POST'):
		data = request.form
		location = Location.query.filter_by(name=data['location'].lower()).first()
		if(not location):
			location = Location(name=data['location'].lower())
			db.session.add(location)
			db.session.commit()
		print(location)
		doc = Doctor(
			name=data['full_name'],
			phone=data['phone'],
			password=data['password'],
			aadhar=data['aadhar'],
			address=data['address'],
			location=location
		)
		db.session.add(doc)
		db.session.commit()
		flash('Successfully Created Account!', 'success')
	
	return render_template('doctor/register.html', title='Doctor Register')

# ----SPACE FOR HOME----
@doctor.route('/home',methods=['GET', 'POST'])
def doctor_home():
	return "HOMEPAGE"

@doctor.route('/logout')
def doctor_logout():
	session['logged_in_doctor'] = None
	return jsonify({})

@doctor.route('/delete_vaccine_batch/<id>')
def delete_vaccine_batch(id):
	vb = VaccineBatch.query.filter_by(id=id).first()
	print("VBBB -> ", vb)
	if(not vb): return jsonify({})
	db.session.delete(vb)
	db.session.commit()
	return ""

@doctor.route('/side_effects')
def get_patient_side_effects():
	doc_id = session.get('logged_in_doctor')
	if(not doc_id): return redirect(url_for('doctor.doctor_login'))
	doctor = Doctor.query.filter_by(id=doc_id).first()
	my_patients = doctor.patients
	side_effects = {}
	for patient in my_patients:
		side_effects[patient.phone] = [
			{
				'symptoms': se.symptoms,
				'description': se.description,
			} for se in patient.side_effects
		]
	print(side_effects)
	return render_template('doctor/side_effects.html', title="Side Effects", patients=my_patients, side_effects=side_effects, json=json)

@doctor.route('/fatalities')
def get_patient_fatalities():
	doc_id = session.get('logged_in_doctor')
	if(not doc_id): return redirect(url_for('doctor.doctor_login'))
	doctor = Doctor.query.filter_by(id=doc_id).first()
	fatalities = [P for P in doctor.patients if P.is_vaccinated and P.is_alive=='0']
	return render_template('doctor/fatalities.html', title="Fatalities", patients=fatalities)

@doctor.route('/mypatients')
def get_my_patients():
	doc_id = session.get('logged_in_doctor')
	if(not doc_id): return redirect(url_for('doctor.doctor_login'))
	doctor = Doctor.query.filter_by(id=doc_id).first()
	patients = doctor.patients
	return render_template('doctor/mypatients.html', title="Fatalities", patients=patients)
