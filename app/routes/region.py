from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
import app.models 
from app.models import ContentSet, Country, Location, Region
from app import db

region= Blueprint('region', __name__, url_prefix='/region')

@region.route('/manage_regions/',methods=['GET','POST'])
def manage_regions():
    if current_user.is_authenticated:
       
        return render_template('manage_regions.html',
                                country = db.session.query(Country).all(),
                                location = db.session.query(Location.country_id).all(),
                                con = db.session.query(ContentSet,Location).join(Location,Location.id==ContentSet.location).all(),
                                region =db.session.query(Region).all(),
                                title='Regions')
                                
# Handles adding country to database(only admins) 
@region.route('/manage_regions/add_region',methods=['GET','POST'])
def add_region():
    if request.method == 'POST':
        rn = request.form['rn'] 
        #Check if country exists in database        
        if db.session.query(Region).filter_by(name = rn).first() is None:
            try:
                region = app.models.Region(name=rn)
                db.session.add(region)
                db.session.commit()
                flash('Region was added!')
                return redirect(url_for('region.manage_regions'))
            except Exception as e:
                flash(str(e))
        else:
            flash(u'region already exists')
            return redirect(url_for('region.manage_regions'))
    return render_template('manage_regions.html',region = db.session.query(Region).all())
#handles editing countries
@region.route('/manage_regions/edit_region/<int:id>',methods=['GET','POST'])
def edit_region(id):
    if request.method == 'POST':    
        name = request.form['rn']
        #Check if country exists in database, we can't have 2 same countries 
        try:
           value = app.models.Region.query.filter_by(id=id).first()
           if db.session.query(Region).filter_by(name = name).first() is None or value.name == name:
                value.name = name
                db.session.commit()
                return redirect(url_for('region.manage_regions'))
           else:
                flash("region already exists")
                return redirect(url_for('region.manage_regions'))
        except Exception as e:
                print(e)
    return redirect(url_for('region.manage_regions'))
#Delete country from database(only admins)
@region.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if current_user.is_authenticated:
        try:
            reg = app.models.Region.query.filter_by(id = id).first()
            db.session.delete(reg)
            db.session.flush()
            db.session.commit()        
            return redirect(url_for('region.manage_regions'))
        except Exception as e:
            print(e)
  
    return redirect(url_for('region.manage_regions'))
            

