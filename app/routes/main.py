from collections import Counter
from unicodedata import name
import pandas as pd
import app
from flask.helpers import flash
from werkzeug.utils import redirect
from app.models import ContentSet, Country, Location, User
from flask import Blueprint, render_template, url_for,request
from flask_login import current_user
from app import db
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.embed import components



main= Blueprint('main', __name__, url_prefix='/')


@main.route('/home/', methods=['GET', 'POST'])
def show():
    if current_user.is_authenticated:
       # output_file("colormapped_bars.html")

        countries = db.session.query(Country.name).join(Location,Location.country_id==Country.id).join(ContentSet,ContentSet.location == Location.id).all()
        x_df = pd.DataFrame(countries)
        x_list = x_df[0].values.tolist()
        x_counter = Counter(x_list)
        x_list = list(x_counter)
        counter_vals = x_counter.values()
        vals_list = list(counter_vals)
        p = figure(x_range = x_list, plot_height=300, plot_width=500,
                                   toolbar_location="right", 
                                   tools="")
        p.vbar(x = x_list, top=vals_list, width=0.9, color=Spectral6)
        p.xgrid.grid_line_color = None
        p.yaxis.axis_label = 'Number of Contents'
        p.y_range.start = 0
        script,div = components(p)       
        kwargs = {'script':script, 'div':div}
        return render_template("home.html", title='home',**kwargs)
      
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
       




