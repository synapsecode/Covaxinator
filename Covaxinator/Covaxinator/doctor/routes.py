from flask import render_template, request, Blueprint
doctor = Blueprint('doctor', __name__)

@doctor.route("/")
def doctor_home():
	return "This is the doctor module of Covaxinator"
