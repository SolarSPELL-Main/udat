
from flask import Blueprint, render_template, url_for,request,flash,redirect
from werkzeug.security import generate_password_hash, check_password_hash
import app.models 
from app import db
from flask_login import login_user,current_user,logout_user
import sqlite3 as sql


user_login= Blueprint('user_login', __name__, url_prefix='/')
#make the login page the first page the user sees when they go to UDAT website
def check_user(username):
            conn = sql.connect('udat.db') # connect to database
            curs = conn.cursor()
            curs.execute("SELECT username FROM User")  
            x = curs.fetchall()
            print(x)
            for i in x:
                if username == i[0]:
                    return True
            return False
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
        if user is not None and request.form['psw1']:
            login_user(user)
            return redirect(url_for('main.show'))
        else:
            flash('You have entered wrong email or password')
        return render_template('user_login.html', title='login')

@user_login.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('user_login.login_user_page',title='login'))

@user_login.route('/manage_users/',methods=['GET','POST'])
def manage_users():
    if current_user.is_authenticated:
        return render_template('manage_users.html',User = app.models.User.query.all(),title='User Managment')
@user_login.route('/manage_users/add_user',methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['un'] # get username input
        password = request.form['pw']
        fullname = request.form['fn']
        is_admin = 0
        if request.form['admin'] is True:
            is_admin = 1
        is_valid = check_user(username)
        if not is_valid:
            try:

                user = app.models.User(fullname=fullname,username=username,password=password,is_admin=is_admin)
                db.session.add(user)
                db.session.commit()
                flash('Data was added!')
                return redirect(url_for('user_login.manage_users'))
            except Exception as e:
                flash(str(e))

        else:
            flash(u'Username already exists')
            return redirect(url_for('user_login.manage_users'))


@user_login.route('/manage_users/edit_user/<int:id>',methods=['GET','POST'])
def edit_user(id):
    
    if request.method == 'POST':    
        fullname = request.form['fn']
        password = request.form['pw']
        username = request.form['un']
        is_valid = check_user(username)
        if not is_valid:
            value = app.models.User.query.filter_by(id=id).first()
            value.username = username
            value.password = password
            value.fullname = fullname
            db.session.commit()
            return redirect(url_for('user_login.manage_users'))
        else:
            flash("Username already exists")
            return redirect(url_for('user_login.manage_users'))

 
    
    
       


@user_login.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        app.models.User.query.filter_by(id=id).delete()
        db.session.commit()
        
        return redirect(url_for('user_login.manage_users'))
    else:
        return render_template("user_login.html", title='login')       



    
             
    