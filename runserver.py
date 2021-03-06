# Main File : This has to be run to start the server

from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack
from views import views
from contest_views import contest_views
from login_views import login_views
from flask.ext.mail import Mail
# Database Configuration
DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'your-gmail-username'
MAIL_PASSWORD = 'your-gmail-password'

# administrator list
ADMINS = ['your-gmail-username@gmail.com']
# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
mail = Mail(app)
# Blueprints : Setting the blueprints for handling various routes 
app.register_blueprint(views)
app.register_blueprint(contest_views)
app.register_blueprint(login_views)

#Initaialzes the database from the database schema give in 'schema.sql'
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
		print db

#Establishes the connection with the database
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

if __name__ == '__main__':
	#init_db()
	app.run(debug=True)
	

