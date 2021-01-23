from flask import render_template, request, Blueprint
patient = Blueprint('patient', __name__)

@patient.route("/")
def patient_home():
	return "This is the patient module of Covaxinator"
