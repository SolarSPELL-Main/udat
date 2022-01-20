import app
from flask.helpers import flash
from werkzeug.utils import redirect
from app.models import User
from flask import Blueprint, render_template, url_for,request
from flask_login import current_user
from app import db


main= Blueprint('main', __name__, url_prefix='/')


@main.route('/home/', methods=['GET', 'POST'])
def show():
    if current_user.is_authenticated:
       return render_template("home.html", title='home')
    else:
       return render_template("user_login.html", title='login')

#Handle manage users button, which returns manage_users html page(only admins) 
@main.route('/manage_users/',methods=['GET','POST'])
def manage_users():
    if current_user.is_authenticated:
        return render_template('manage_users.html',
                                User = app.models.User.query.all(),
                                title='User Managment',
                                currentUser = current_user.fullname)

# Handle adding user to database(only admins) 
@main.route('/manage_users/add_user',methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['un'] 
        password = request.form['pw']
        fullname = request.form['fn']
        is_admin = 0
        if request.form.get("admin"):
            is_admin = 1
        #Check if username exists in database, we can't have 2 same usernames
        #is_valid = check_user(username, id)
        if db.session.query(User).filter_by(username = username).first() is None:
            try:
                user = app.models.User(fullname=fullname,username=username,password=password,is_admin=is_admin)
                db.session.add(user)
                db.session.commit()
                flash('User was added!')
                return redirect(url_for('main.manage_users'))
            except Exception as e:
                flash(str(e))
        else:
            flash(u'Username already exists')
            return redirect(url_for('main.manage_users'))
        return redirect(url_for('main.manage_users'))

#Edit user saved in database (only admins)
@main.route('/manage_users/edit_user/<int:id>',methods=['GET','POST'])
def edit_user(id):
   if request.method == 'POST':    
        fullname = request.form['fn']
        password = request.form['pw']
        username = request.form['un']
        #Check if username exists in database, we can't have 2 same usernames 
        try:
           value = app.models.User.query.filter_by(id=id).first()
           if db.session.query(User).filter_by(username = username).first() is None or value.username == username:
                value.username = username
                value.password = password
                value.fullname = fullname
                db.session.commit()
                return redirect(url_for('main.manage_users'))
           else:
                flash("Username already exists")
                return redirect(url_for('main.manage_users'))
        except Exception as e:
                print(e)
   return redirect(url_for('main.manage_users'))
  
@main.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        try:
            app.models.User.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect(url_for('main.manage_users'))
        except Exception as e:
            print(e)  
    return redirect(url_for('main.manage_users'))
       




