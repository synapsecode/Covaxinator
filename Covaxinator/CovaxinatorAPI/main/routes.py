from flask import render_template, request, Blueprint, url_for, redirect, flash, jsonify, session
from CovaxinatorAPI.models import *
from CovaxinatorAPI.config import Config
from werkzeug.utils import secure_filename
import os
import json
# from CovaxinatorAPI import socketio
# from flask_socketio import send

main = Blueprint('main', __name__)

@main.route("/")
def main_home():
	return render_template('main.html', title='Covaxinator')

@main.route('/home', methods=['GET', 'POST'])
def home():
	shield_data = {}
	for L in Location.query.all():
		vac = len([P for P in L.patients.all() if P.is_vaccinated])
		unvac = len([P for P in L.patients.all() if not P.is_vaccinated])
		total = vac+unvac if vac+unvac > 0 else 1
		print([P for P in L.patients])
		shield_data[L.name] = {
			'vaccinated': vac,
			'notvaccinated':unvac,
			'shieldpoint': round((vac/total)*100,3),
		}
	shield_data = json.dumps(shield_data)
	return render_template('general.html', shield_data=shield_data, json=json)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@main.route('/facescan', methods=['GET', 'POST'])
def facescan():
	if(request.method == 'POST'):
		if('file' not in request.files):
			flash('No Uploaded Image', 'danger')
			return redirect(redirect.url)
		file = request.files['file']
		if(file.filename == ''):
			flash('No selected file', 'danger')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
	return render_template('facescan.html')

@main.route('/getcertificate/<patientphone>')
def getcertificate(patientphone):
	patientphone = patientphone.replace('%2B','+')
	print(patientphone)
	
	shield_data = json.dumps(shield_data)
	return jsonify({"redirect": url_for('patient.get_vaccination_certificate', phone=patientphone)})