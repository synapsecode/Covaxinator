from flask import render_template, request, Blueprint, url_for, redirect, flash, jsonify, session
from CovaxinatorAPI.models import *
# from CovaxinatorAPI import socketio
# from flask_socketio import send

main = Blueprint('main', __name__)

@main.route("/")
def main_home():
	return render_template('main.html', title='Covaxinator')

@main.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('general.html')

@main.route('/facescan', methods=['GET', 'POST'])
def facescan():
	return render_template('facescan.html')

@main.route('/getcertificate/<patientphone>')
def getcertificate(patientphone):
	return redirect(url_for('patient.get_vaccination_certificate', phone=patientphone))