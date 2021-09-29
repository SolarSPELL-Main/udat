from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
import app.models 
from app.models import ContentSet, Country, Location
from app import db

countries= Blueprint('countries', __name__, url_prefix='/countries')

@countries.route('/manage_countries/',methods=['GET','POST'])
def manage_countries():
    if current_user.is_authenticated:
        return render_template('manage_countries.html',
                                country = db.session.query(Country).all(),
                                location = db.session.query(Location.country_id).all(),
                                con = db.session.query(ContentSet.location).all(),
                                title='Countries')
                                
# Handles adding country to database(only admins) 
@countries.route('/manage_countries/add_country',methods=['GET','POST'])
def add_country():
    if request.method == 'POST':
        cn = request.form['cn1'] 
        #Check if country exists in database        
        if db.session.query(Country).filter_by(name = cn).first() is None:
            try:
                country = app.models.Country(name=cn)
                db.session.add(country)
                db.session.commit()
                flash('Country was added!')
                return render_template('manage_countries.html',country = db.session.query(Country).all())
            except Exception as e:
                flash(str(e))
        else:
            flash(u'Username already exists')
            return render_template('manage_countries.html',country = db.session.query(Country).all())
    return render_template('manage_countries.html',country = db.session.query(Country).all())
#handles editing countries
@countries.route('/manage_countries/edit_country/<int:id>',methods=['GET','POST'])
def edit_country(id):
    if request.method == 'POST':    
        name = request.form['cn']
        #Check if country exists in database, we can't have 2 same countries 
        try:
           value = app.models.Country.query.filter_by(id=id).first()
           if db.session.query(Country).filter_by(name = name).first() is None or value.name == name:
                value.name = name
                db.session.commit()
                return redirect(url_for('countries.manage_countries'))
           else:
                flash("Username already exists")
                return redirect(url_for('countries.manage_countries'))
        except Exception as e:
                print(e)
    return redirect(url_for('countries.manage_countries'))
#Delete country from database(only admins)
@countries.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        try:
            con = app.models.Country.query.filter_by(id = id).first()
            db.session.delete(con)
            db.session.flush()
            db.session.commit()
        
            return redirect(url_for('countries.manage_country'))
        except Exception as e:
            print(e)
  
    return redirect(url_for('countries.manage_countries'))
            

