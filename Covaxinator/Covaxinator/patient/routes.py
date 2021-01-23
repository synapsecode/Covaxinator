from flask import render_template, request, Blueprint, flash, url_for, redirect, jsonify, flash, session
import json
from Covaxinator.models import *
from Covaxinator import db

patient = Blueprint('patient', __name__)

@patient.route('/login', methods=['GET', 'POST'])
def patient_login():
	if(request.method == 'POST'):
		data = request.form
		phone = data['phone']
		password = data['password']
		patient = Patient.query.filter_by(phone=phone).first()
		if(not patient or patient.password != password):
			print("INVALID")
			flash('Invalid Credentials!', 'danger')
			return jsonify({"redirect": url_for('patient.patient_login')})

		flash('Login Completed Successfully!', 'success')
		session['logged_in_patient'] = patient.id
		return jsonify({"redirect": url_for('patient.patient_home')})
	return render_template('patient/login.html', title='Patient Login')

@patient.route('/register', methods=['GET', 'POST'])
def patient_register():
	if(request.method == 'POST'):
		data = request.form
		location = Location.query.filter_by(name=data['location'].lower()).first()
		if(not location):
			location = Location(name=data['location'].lower())
			db.session.add(location)
			db.session.commit()
		print(location)
		pat = Patient(
			name=data['full_name'],
			phone=data['phone'],
			password=data['password'],
			aadhar=data['aadhar'],
			address=data['address'],
			location=location
		)
		db.session.add(pat)
		db.session.commit()
		flash('Successfully Created Account!', 'success')
	
	return render_template('patient/register.html', title='Patient Register')

# ---------PATIENT HOME---------------
@patient.route('/home',methods=['GET', 'POST'])
def patient_home():
	return "HOMEPAGE"

@patient.route('/logout')
def patient_logout():
	session['logged_in_patient'] = None
	return jsonify({})


@patient.route('/report_fatality')
def report_fatality():
	pat_id = session.get('logged_in_patient')
	if(not pat_id): return redirect(url_for('patient.patient_login'))
	print("Reporting Death")
	patient = Patient.query.filter_by(id=pat_id).first()
	if(not patient.is_vaccinated):
		flash('You have not been vaccinated', 'danger')
		return redirect(url_for('patient.patient_home'))
	patient.is_alive = False
	db.session.commit()
	return redirect(url_for('patient.patient_home'))


@patient.route('/vaccination_certificate/<phone>')
def get_vaccination_certificate(phone):
	patient = Patient.query.filter_by(phone=phone).first()
	if(not patient): return "NO SUCH PATIENT"
	if(not patient.is_vaccinated): return "PATIENT NOT VACCINATED"

	vaccine_batch = patient.vaccine_batch
	

	return render_template('patient/certificate.html', title="Vaccination Certificate", patient=patient, vaccine_batch=vaccine_batch)

@patient.route('/report_symptoms', methods=['POST'])
def report_symptoms():
	pat_id = session.get('logged_in_patient')
	if(not pat_id): return redirect(url_for('patient.patient_login'))
	data = request.form
	patient_phone = data['patient_phone']
	symptoms = data['symptoms'].split(',')
	description = data['symdesc']
	patient = Patient.query.filter_by(phone=patient_phone).first()
	if(not patient): return "NO SUCH PATIENT"
	if(not patient.is_vaccinated):
		flash('You have not been vaccinated', 'danger')
		return jsonify({'redirect': url_for('patient.patient_home')})
	patient.report_side_effects(symptoms, description)
	return jsonify({'redirect': url_for('patient.patient_home')})
