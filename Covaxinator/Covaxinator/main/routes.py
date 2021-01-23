from flask import render_template, request, Blueprint
main = Blueprint('main', __name__)

@main.route("/")
def main_home():
	return render_template('main.html', title='Covaxinator')
