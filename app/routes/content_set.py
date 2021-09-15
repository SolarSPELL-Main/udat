import datetime
from re import L
from flask import Blueprint, render_template,flash, request,url_for,jsonify
from sqlalchemy.orm import session
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.schema import Column
from app.models import Content, ContentSet, Country, Location, User
from app import db
import csv
from io import TextIOWrapper
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import current_user
import os
import json




content_set= Blueprint('content_set', __name__, url_prefix='/')

# This is where the routes and their defenitions will go 

# # For add_content_set
@content_set.route('/select_country', methods=['GET','POST'])
def select_country():
    country = request.args.get('country',type=str)
    con_id = db.session.query(Country.id).filter_by(name=country).all()
    locations = db.session.query(Location.name).filter_by(country_id = con_id[0][0]).all()
    ret = ''
    for entry in locations:
        ret += '<option value="{}">{}</option>'.format(entry[0],entry[0])
    return jsonify(ret=ret)

                               
                                      
  
@content_set.route('/add', methods=['GET','POST'])
def upload():
    if current_user.is_authenticated:
        if request.method == 'POST':
            i=0
            content_sets= []
            is_file_valid=None
            #Uploading multiple CSV
            for file in request.files.getlist("csvfiles"):
                csv_files = TextIOWrapper(file, encoding='utf-8-sig')
                temp = csv_files.read()
                content_sets.append(temp)
                #checking valid CSV File
                isRowLenValid =  len(temp.split("\n")) > 1 
                file_size=get_file_size(file)
                if(file_size!=0):
                    is_file_valid=True
                is_file_valid = isRowLenValid         
            if(is_file_valid):   
                Exported_date = str(request.form['Exported on'])
                year, month, day = map(int, Exported_date.split('-'))
                filter_Exported_date = datetime.date(year, month, day)
                Imported_date = str(request.form['Imported on'])
                year1, month1, day1 = map(int, Imported_date.split('-'))
                filter_Imported_date = datetime.date(year1, month1, day1)
                #location
                loc = request.form.get('Location')
                loc_id = db.session.query(Location.id).filter_by(name=loc).all()  
                content_set = ContentSet(exported_on=filter_Exported_date,
                                         imported_on=filter_Imported_date,
                                         lib_version=request.form['Library version'],
                                         imported_by=current_user.id)

                db.session.add(content_set)
                content_set.location = loc_id[0][0]
                db.session.commit()
                
                ## Fetch the new ID
                newid=content_set.id
             
                for i in range(len(content_sets)):
                    contentval = prepare_content_object(newid,csv.DictReader(content_sets[i].splitlines(), skipinitialspace=True))
                    db.session.bulk_insert_mappings(Content,contentval)
                    db.session.commit()
                
                return redirect(url_for('content_set.show_all'))
            else:
                flash('Invalid CSV file,Please check and retry!')
        
        return redirect(url_for('content_set.show_all'))
    else:
        return render_template("user_login.html",
                               title='SolarSpell')

# Method to decode and set ID for FK
def prepare_content_object(new_id, content_csv_obj):
    content_list = []
    for row in content_csv_obj:
        file_items=row.items()
        content_obj = {}
        for k, v in file_items:
            content_obj[k] = v
        content_obj['set_id'] = new_id
        content_list.append(content_obj)
    return content_list 
    

## For edit_content_set
@content_set.route('/edit_content_set/edit_content/<int:id>', methods=['GET','POST'])
def edit_content(id):
    if current_user.is_authenticated:
        # fetch corresponding dataset from DB
        if request.method == 'POST':
            content_set_rec = db.session.get(ContentSet, {"id": id})
            return render_template('edit_content_set.html',
                                 id = id
                                ,location=content_set_rec.location
                                ,exported_on=content_set_rec.exproted_on
                                ,imported_on=content_set_rec.imported_on
                                ,lib_version = content_set_rec.lib_version
                                ,countries=db.session.query(Country.name).all()
                                )
        return redirect(url_for('content_set.show_all'))
    else:
        return redirect(url_for('main.show'))

           
@content_set.route('/edit_content_set/save_content/<int:id>', methods=['GET','POST'])
def save_edited_content(id):
    if request.method == 'POST':
        # Handle from DB
        Exported_date = str(request.form['Exported_on'])
        year, month, day = map(int, Exported_date.split('-'))
        export_date = datetime.date(year, month, day)
        Imported_date = str(request.form['Imported_on'])
        year1, month1, day1 = map(int, Imported_date.split('-'))
        import_date = datetime.date(year1, month1, day1)
        location = request.form['location']
        lib_version=request.form['Library_version']

        # Updating the content_set
        value = ContentSet.query.filter_by(id=id).first()            
        value.location = location
        value.exproted_on = export_date
        value.lib_version = lib_version
        value.imported_on = import_date
        db.session.commit()                         
        return redirect(url_for('content_set.show_all'))
    return redirect(url_for('content_set.show_all'))

## For Delete content_set
@content_set.route('/delete/<int:id1>', methods=['GET','POST'])
def delete(id1):
    if current_user.is_authenticated:
        content_set = ContentSet.query.filter_by(id=id1).first()
        db.session.delete(content_set)
        db.session.flush()
        db.session.commit()
        
        return redirect(url_for('content_set.show_all'))
    else:
        return render_template("user_login.html", title='login')

## For show_all
@content_set.route('/show_all')
def show_all():
    if current_user.is_authenticated:
        return render_template('show_all.html',ContentSet = db.session.query(ContentSet, Location,Country).\
                                               join(Location,Location.id == ContentSet.location).\
                                               join(Country, Country.id == Location.country_id).all()
                                ,country = db.session.query(Country.name).all(), title='Show Content')
    else:
        return render_template("user_login.html", title='login')


def is_file_valid(file_size):
    if (file_size!=0):
        return True
def get_file_size(file):
    file_size=0
    file.seek(0,os.SEEK_END)
    file_size=file.tell()
    return file_size

