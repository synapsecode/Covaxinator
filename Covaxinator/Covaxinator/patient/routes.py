from flask import render_template, request, Blueprint
patient = Blueprint('patient', __name__)

@patient.route('/login', methods=['GET', 'POST'])
def patient_login():
	return "LOGIN"

@patient.route('/register', methods=['GET', 'POST'])
def patient_register():
	return "REGISTER"