from flask import Blueprint, render_template, flash
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.utils import redirect
from app.models import Content, ContentSet
from app import db

content_set= Blueprint('content_set', __name__, url_prefix='/content_set')

# This is where the routes and their defenitions will go

 


@content_set.route('/delete/<int:id1>', methods=['GET','POST'])
def delete(id1):
    ContentSet.query.filter_by(id=id1).delete()
    db.session.commit()
    flash('1 content set was deleted successfully', 'success')
    return redirect(url_for('content_set.show_all'))
    

@content_set.route('/show_all')
def show_all():
    return render_template('show_all.html',ContentSet = ContentSet.query.all(), title='Show Content')



  
@content_set.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
     return render_template('edit.html', title='Edit content set')
     

@content_set.route('/add', methods=['GET','POST'])
def add():
    return render_template('add.html', title='Add content Set')