from flask import render_template, request, Blueprint, url_for, redirect, flash, jsonify, session
from CovaxinatorAPI.models import *
# from CovaxinatorAPI import socketio
# from flask_socketio import send

main = Blueprint('main', __name__)

@main.route("/")
def main_home():
	return render_template('main.html', title='Covaxinator')

