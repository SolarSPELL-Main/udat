import datetime
from flask import Blueprint, render_template,flash, request
from sqlalchemy.orm import session
from app.models import Content, ContentSet
from app import db
import pandas as pd
from werkzeug.utils import secure_filename
import csv
import pandas as pd
from io import TextIOWrapper
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.utils import redirect
from flask_login import current_user



content_set= Blueprint('content_set', __name__, url_prefix='/content_set')

# This is where the routes and their defenitions will go 

# For add_content_set

@content_set.route('/add', methods=['GET','POST'])
def upload():
    if current_user.is_authenticated:
        if request.method == 'POST':

            csv_file = request.files['csvfiles']
            # filename = secure_filename(csv_file.filename)
            csv_files = TextIOWrapper(csv_file, encoding='utf-8-sig')
            content_sets = csv_files.read() # read csv file
            Exported_date = str(request.form['Exported on'])
            year, month, day = map(int, Exported_date.split('-'))
            filter_Exported_date = datetime.date(year, month, day)

            Imported_date = str(request.form['Imported on'])
            year1, month1, day1 = map(int, Imported_date.split('-'))
            filter_Imported_date = datetime.date(year1, month1, day1)
            content_set = ContentSet(location=request.form['Location'],exported_on=filter_Exported_date, imported_on=filter_Imported_date, imported_by=request.form['Imported by'], lib_version=request.form['Library version'])


            db.session.add(content_set)
            db.session.commit()
            
            # Fetch the new ID
            newid=content_set.id
            content_list = prepare_content_object(newid,csv.DictReader(content_sets.splitlines(), skipinitialspace=True))
            db.session.bulk_insert_mappings(Content,content_list)
            db.session.commit()
            flash('Data was added!')
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
    print('Content_List ',content_list)
    return content_list    

# For edit_content_set

# @content_set.route('/edit/<int:id>', methods=['GET','POST'])
# def edit(id):
    #  return render_template('edit.html', title='Edit content set')

@content_set.route('/edit_content_set/', methods=['GET','POST'])
def edit_content():
    if current_user.is_authenticated:

    
        # http://127.0.0.1:5000/content_set/edit_content_set/?id=123

        # # fetch Id from request parameter, if not given, defaults to 1 for testing purposes now

        # print('ans for update ', request.args.get('id'))
        content_set_id = request.args.get('id') if request.args.get('id') is not None else 1

        # # fetch corresponding dataset from DB
        
        if request.method == 'POST':
            content_set_rec = db.session.get(ContentSet, {"id": content_set_id})

            # render in UI for Edit modal
            return render_template('edit_content_set.html',
                                
                                location=content_set_rec.location,
                                exported_on=content_set_rec.exproted_on,
                                imported_on=content_set_rec.imported_on,
                                imported_by=content_set_rec.imported_by,
                                lib_version = content_set_rec.lib_version
                                )
            
        else:
            # Handle from DB
            
            Exported_date = str(request.form['Exported_on'])
            year, month, day = map(int, Exported_date.split('-'))
            export_date = datetime.date(year, month, day)

            Imported_date = str(request.form['Imported_on'])
            year1, month1, day1 = map(int, Imported_date.split('-'))
            import_date = datetime.date(year1, month1, day1)

            content_set = ContentSet(location=request.form['Location'], exported_on=export_date, imported_on=import_date,
                                    imported_by=request.form['Imported_by'], lib_version=request.form['Library_version'])

            print('update now' ,content_set_id)
            # Updating the content_set
            value = ContentSet.query.filter_by(id=content_set_id).first()
            
            value.location = content_set.location
            value.export_date = content_set.exproted_on
            value.lib_version = content_set.lib_version
            value.imported_by = content_set.imported_by
            value.imported_on = content_set.imported_on

            db.session.commit()                         

            return render_template('edit_content_set.html')
    else:
        return render_template("user_login.html", title='login')

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

