from flask import Blueprint, render_template, flash
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.utils import redirect
from app.models import Content, ContentSet
from app import db
from flask_login import current_user
content_set= Blueprint('content_set', __name__, url_prefix='/content_set')

# This is where the routes and their defenitions will go
@content_set.route('/delete/<int:id1>', methods=['GET','POST'])
def delete(id1):
    if current_user.is_authenticated:
        ContentSet.query.filter_by(id=id1).delete()
        db.session.commit()
        
        return redirect(url_for('content_set.show_all'))
    else:
        return render_template("user_login.html", title='SolarSpell')
  
@content_set.route('/show_all')
def show_all():
    if current_user.is_authenticated:
        return render_template('show_all.html',ContentSet = ContentSet.query.all(), title='Show Content')
    else:
        return render_template("user_login.html", title='SolarSpell')

@content_set.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if current_user.is_authenticated:
        return render_template('edit.html', title='Edit content set')
    else:
        return render_template("user_login.html", title='SolarSpell')
     
@content_set.route('/add', methods=['GET','POST'])
def add():
    if current_user.is_authenticated:
        return render_template('add.html', title='Add content Set')
    else:
        return render_template("user_login.html", title='SolarSpell')
