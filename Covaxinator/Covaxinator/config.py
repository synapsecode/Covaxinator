import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = "2F5F6CE5hfbhfb0B54AA5D7CED1BA56698fbhbhbdbhbA2814A51CE1865D2C2D8815CD4"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') #Database path
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	PRODUCTION_MODE = False #This states whether the app runs in DEBUG MODE or not
	PORT_NUMBER = 5000
	HOST_NAME = 'localhost'
