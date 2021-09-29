
from flask import Blueprint, render_template, url_for,request,flash,redirect
import app.models 
from app import db
from flask_login import login_user,current_user,logout_user
from app.models import User


#Make the login page the first page the user sees when they go to UDAT website
user_login = Blueprint('user_login', __name__, url_prefix='/')


#Return login page if user is not logged in, and if user is logged in it will return home
@user_login.route('/')
def login_user_page():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('user_login.html', title = 'login')


#Handle the login authentication
@user_login.route('/', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.show'))
    if request.method == 'POST':
        username = request.form['uname1'] # get username input
        password = request.form['psw1'] # get password input
        user = app.models.User.query.filter(app.models.User.username == username, 
                                            app.models.User.password == password).first()
        if user is not None and request.form['psw1']:
            login_user(user)
            return redirect(url_for('main.show'))
        else:
            flash('You have entered wrong email or password')
        return render_template('user_login.html', title ='login')


#Handle user logout 
@user_login.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('user_login.login_user_page',title='login'))







            


#Delete user from database(only admins)
@user_login.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        try:
            app.models.User.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect(url_for('user_login.manage_users'))
        except Exception as e:
            print(e)
    else:
        return render_template("user_login.html", title='login')     

@user_login.route('/admin_tool/',methods=['GET','POST'])
def admin_tool():
    if current_user.is_authenticated:
        return render_template('admin_tool.html',
                                
                                title='Admin Tool')






    
             
    