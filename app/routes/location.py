from os import name
from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
import app.models 
from app.models import ContentSet, Country, Location
from app import db

location= Blueprint('location', __name__, url_prefix='/location')

@location.route('/manage_locations/',methods=['GET','POST'])
def manage_locations():
    if current_user.is_authenticated:
        countries = db.session.query(Country.name).group_by("name").all()
        return render_template('manage_location.html',
                             locations = db.session.query(Location, Country).join(Country,Country.id == Location.country_id).all(),
                             countries = countries,
                             contents = db.session.query(ContentSet.location).all(),
                             title='Locations')

@location.route('/manage_location/add_location',methods=['GET','POST'])
def add_location():
    if request.method == 'POST':
        name = request.form['ln'] 
        country = request.form.get('coun')
        country_id = db.session.query(Country.id).filter_by(name=country).all()
        #Check if location exists in database        
        if db.session.query(Location).filter_by(name = name).first() is None:
            try:
                location= app.models.Location(name=name)
                db.session.add(location)
                location.country_id = country_id[0][0]
                db.session.commit()
                flash('location was added!')
                return redirect(url_for('location.manage_locations'))
            except Exception as e:
                flash(str(e))
        else:
            flash(u'Location already exists')
            return redirect(url_for('location.manage_locations'))
    return redirect(url_for('location.manage_locations'))

@location.route('/manage_locations/edit_location/<int:id>',methods=['GET','POST'])
def edit_location(id):
    if request.method == 'POST':    
        name = request.form['ln']
        country_name = request.form['Country']
        country_id = db.session.query(Country.id).filter_by(name=country_name).all()
        #Check if username exists in database, we can't have 2 same usernames 
        try:
           value = app.models.Location.query.filter_by(id=id).first()
           if db.session.query(Location).filter_by(name = name).first() is None or value.name == name:
                value.name = name
                value.country_id = country_id[0][0]
                db.session.commit()
                return redirect(url_for('location.manage_locations'))
           else:
                flash("Location already exists")
                return redirect(url_for('location.manage_locations'))
        except Exception as e:
                print(e)
    return redirect(url_for('location.manage_locations'))

#Delete country from database(only admins)
@location.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        try:
            loc = app.models.Location.query.filter_by(id = id).first()
            db.session.delete(loc)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('location.manage_locations'))
        except Exception as e:
            print(e)
  
    return redirect(url_for('location.manage_locations'))