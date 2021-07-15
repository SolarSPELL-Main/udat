import datetime
from flask import Blueprint, render_template,flash, request,url_for
from sqlalchemy.orm import session
from sqlalchemy import join
from sqlalchemy.sql import select
from app.models import Content, ContentSet, User
from app import db
import pandas as pd
from werkzeug.utils import secure_filename
import csv
from io import TextIOWrapper
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.utils import redirect
from flask_login import current_user



content_set= Blueprint('content_set', __name__, url_prefix='/content_set')

# This is where the routes and their defenitions will go 

# # For add_content_set

@content_set.route('/add', methods=['GET','POST'])
def upload():
    if current_user.is_authenticated:
        if request.method == 'POST':

            csv_file = request.files['csvfiles']
            csv_files = TextIOWrapper(csv_file, encoding='utf-8-sig')
            content_sets = csv_files.read() # read csv file
            Exported_date = str(request.form['Exported on'])
            year, month, day = map(int, Exported_date.split('-'))
            filter_Exported_date = datetime.date(year, month, day)

            Imported_date = str(request.form['Imported on'])
            year1, month1, day1 = map(int, Imported_date.split('-'))
            filter_Imported_date = datetime.date(year1, month1, day1)
            
            content_set = ContentSet(location=request.form['Location']
                                    ,exported_on=filter_Exported_date
                                    , imported_on=filter_Imported_date
                                    ,lib_version=request.form['Library version'],imported_by=current_user.id)
            db.session.add(content_set)
            db.session.commit()
            
            
            # Fetch the new ID
            newid=content_set.id
            content_list = prepare_content_object(newid,csv.DictReader(content_sets.splitlines(), skipinitialspace=True))
            db.session.bulk_insert_mappings(Content,content_list)
            db.session.commit()
            return redirect(url_for('content_set.show_all'))
            
            # flash('Data was added!')
        return render_template('add_content_set.html')
    else:
        return render_template("user_login.html", title='SolarSpell')

def prepare_content_object(new_id, content_csv_obj):
    
    # Method to decode and set ID for FK
    
    content_list = []
    for row in content_csv_obj:
        content_obj = {}
        for k, v in row.items():
            content_obj[k] = v

        content_obj['set_id'] = new_id
        content_list.append(content_obj)
    return content_list    

# # For edit_content_set
@content_set.route('/edit_content_set/edit_content/<int:id>', methods=['GET','POST'])
def edit_content(id):
    if current_user.is_authenticated:
        # # fetch corresponding dataset from DB
        if request.method == 'POST':
            content_set_rec = db.session.get(ContentSet, {"id": id})
            return render_template('edit_content_set.html',
                                id = id,
                                location=content_set_rec.location,
                                exported_on=content_set_rec.exproted_on,
                                imported_on=content_set_rec.imported_on,
                                # imported_by=content_set_rec.imported_by,
                                lib_version = content_set_rec.lib_version
                                )
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
        location = request.form['Location']
        # imported_by=request.form['Imported_by']
        imported_by=current_user.id
        lib_version=request.form['Library_version']

        # Updating the content_set
        value = ContentSet.query.filter_by(id=id).first()            
        value.location = location
        value.exproted_on = export_date
        value.lib_version = lib_version
        # value.imported_by = imported_by
        value.imported_on = import_date
        db.session.commit()                         
        return redirect(url_for('content_set.show_all'))
    return redirect(url_for('content_set.show_all'))

@content_set.route('/delete/<int:id1>', methods=['GET','POST'])
def delete(id1):
    if current_user.is_authenticated:
        ContentSet.query.filter_by(id=id1).delete()
        db.session.commit()
        
        return redirect(url_for('content_set.show_all'))
    else:
        return render_template("user_login.html", title='login')

@content_set.route('/show_all')
def show_all():
    
    if current_user.is_authenticated:
        return render_template('show_all.html',ContentSet = ContentSet.query.all(), title='Show Content')
    else:
        return render_template("user_login.html", title='login')

