from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
import app.models 
from app.models import ContentSet, Country, Location, Region
from app import db

countries= Blueprint('countries', __name__, url_prefix='/countries')

@countries.route('/manage_countries/',methods=['GET','POST'])
def manage_countries():
    if current_user.is_authenticated:
        return render_template('manage_countries.html',
                                country = db.session.query(Country,Region).join(Region,Region.id == Country.region_id).all(),
                                location = db.session.query(Location).all(),
                                con = db.session.query(ContentSet.location).all(),
                                reg = db.session.query(Region.name).group_by("name").all(),
                                title='Countries')
                                
# Handles adding country to database(only admins) 
@countries.route('/manage_countries/add_country',methods=['GET','POST'])
def add_country():
    if request.method == 'POST':
        cn = request.form['cn'] 
        region = request.form.get('reg')
        region_id = db.session.query(Region.id).filter_by(name=region).all()
        #Check if country exists in database        
        if db.session.query(Country).filter_by(name = cn).first() is None:
            try:
                country = app.models.Country(name=cn)
                db.session.add(country)
                country.region_id = region_id[0][0]
                db.session.commit()
                flash('Country was added!')
                return redirect(url_for('countries.manage_countries'))
            except Exception as e:
                flash(str(e))
        else:
            flash(u'Country already exists')
            return redirect(url_for('countries.manage_countries'))
    return render_template('manage_countries.html',country = db.session.query(Country).all())
#handles editing countries
@countries.route('/manage_countries/edit_country/<int:id>',methods=['GET','POST'])
def edit_country(id):
    if request.method == 'POST':    
        name = request.form['cn']
        region_name = request.form['Region']
        region_id = db.session.query(Region.id).filter_by(name=region_name).all()
        #Check if country exists in database, we can't have 2 same countries 
        try:
           value = app.models.Country.query.filter_by(id=id).first()
           if db.session.query(Country).filter_by(name = name).first() is None or value.name == name:
                value.name = name
                value.region_id = region_id[0][0]
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
            

