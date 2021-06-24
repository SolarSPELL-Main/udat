
from flask import Blueprint, render_template, url_for,request,flash,redirect
from werkzeug.security import generate_password_hash, check_password_hash
import app.models 
from flask_login import login_user


user_login= Blueprint('user_login', __name__, url_prefix='/')

@user_login.route('/')
def login_user_page():
    return render_template('user_login.html')

@user_login.route('/', methods=['POST','GET'])
def login():
   
    if request.method == 'POST':
        username = request.form['uname1'] # get username input
        password = request.form['psw1'] # get password input
        user = app.models.User.query.filter(app.models.User.username==username, app.models.User.password==password).first()
        if user is not None and request.form['psw1']:
            login_user(user)
            return redirect(url_for('main.show'))
       
    return render_template('user_login.html')
    
    