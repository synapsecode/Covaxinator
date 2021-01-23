from flask import render_template, request, Blueprint
from Covaxinator.models import *
from Covaxinator import db

doctor = Blueprint('doctor', __name__)

@doctor.route('/login', methods=['GET', 'POST'])
def doctor_login():
	return "LOGIN"

@doctor.route('/register', methods=['GET', 'POST'])
def doctor_register():
	return "REGISTER"