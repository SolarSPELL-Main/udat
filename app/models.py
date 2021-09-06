from app import db
from flask_login import UserMixin

# the class references the content set imprted into the database
class ContentSet(db.Model):
    __tablename__ = 'content_set'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.Integer, db.ForeignKey('location.id'))
    exproted_on = db.Column(db.Date()) # When was the content set exported from the library
    imported_on = db.Column(db.Date()) # automatically generated 
    imported_by = db.Column(db.Integer, db.ForeignKey('user.id')) # the name of user who imported the content set 
    lib_version = db.Column(db.String(20)) # Library version 
    content = db.relationship("Content", cascade="all, delete")
  
    def __init__(self, exported_on, imported_on ,lib_version, imported_by):
        self.exproted_on = exported_on
        self.imported_on = imported_on
        self.lib_version = lib_version
        self.imported_by=imported_by
        
# the class refrence users table in database
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean)
    user_ids = db.relationship(ContentSet, backref='user', lazy = 'select' , uselist = False)
    
    def __init__(self,fullname,username,password,is_admin):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.is_admin = is_admin

# the class references the Content table in the database
class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    language = db.Column(db.String(50))
    content_type = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    parent_folder = db.Column(db.String(100))
    browser = db.Column(db.String(50))
    device_type = db.Column(db.String(50))
    device_os = db.Column(db.String(50))
    set_id = db.Column(db.Integer, db.ForeignKey('content_set.id'))

    def __init__(self, title, language, content_type, subject, parent_folder, browser, device_type, device_os):
        self.title = title
        self.language = language
        self.content_type = content_type
        self.subject = subject
        self.parent_folder = parent_folder
        self.browser = browser
        self.device_type = device_type
        self.device_os = device_os

# the class references the Country table in the database
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    location = db.relationship("Location", cascade="all, delete")

    def __init__(self,name):
        self.name = name

# the class references the Location table in the database
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    contentset = db.relationship("ContentSet", cascade="all, delete")

    def __init__(self,name):
        self.name = name
  

    
