
from flask import Blueprint, render_template, url_for,request,flash,redirect
from werkzeug.security import generate_password_hash, check_password_hash
import app.models 
from flask_login import login_user,current_user,logout_user


user_login= Blueprint('user_login', __name__, url_prefix='/')
#make the login page the first page the user sees when they go to UDAT website
@user_login.route('/')
def login_user_page():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('user_login.html', title='login')

#handle the login authentication
@user_login.route('/', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return render_template('home.html')
    if request.method == 'POST':
        username = request.form['uname1'] # get username input
        password = request.form['psw1'] # get password input
        user = app.models.User.query.filter(app.models.User.username==username, app.models.User.password==password).first()
        fullname = user.fullname
        if user is not None and request.form['psw1']:
            login_user(user)
            return redirect(url_for('main.show'))
            session['fullname']=fullname
        else:
            flash('You have entered wrong email or password')
        return render_template('user_login.html', title='login')

@user_login.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('user_login.login_user_page',title='login'))

    
    