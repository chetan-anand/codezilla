from sqlite3 import dbapi2 as sqlite3
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from flask.ext.mail import Message
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'your-gmail-username'
MAIL_PASSWORD = 'your-gmail-password'

# administrator list
ADMINS = ['your-gmail-username@gmail.com']


################## initializing database ########################
def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect('database.db')
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db
	return top.sqlite_db
#################################################################


################################### function for the confirmation email########
def confirm_mail(email):
    """
    Send the awaiting for confirmation mail to the user.
    """
    print email
    subject = "We're waiting for your confirmation!!"
    message = Message(subject=subject, recipients=[email])
    #confirmation_url = url_for('activate_user', user_id=email, _external=True)
    #print confirmation_url
    #message.body = "Dear %s, Please click here to complete your registration process %s" %(email, confirmation_url)
    from runserver import mail
    mail.send(message)
    
##############################  function for the forgot email ############
    
def forgot_mail(mail):
    """
    Send the awaiting for confirmation mail to the user.
    """
    print mail
    '''subject = "We're waiting for your confirmation!!"
    message = Message(subject=subject, recipients=[email])
    db=get_db
    cur=db.execute('select * from users where email='mail'')
    rows=cur.fetchone()
    print rows[1]
    print rows[2]'''
    #confirmation_url = url_for('activate_user', user_id=email, _external=True)
    #print confirmation_url
    #message.body = "Dear %s, Please click here to complete your registration process %s" %(email, confirmation_url)
    from runserver import mail
    #mail.send(message)
