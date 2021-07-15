from bokeh.models.annotations import Title
from app.routes.user_login import login
from datetime import datetime
from datetime import date
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import backref, relationship




# the class references the content set imprted into the database
class ContentSet(db.Model):
    __tablename__ = 'content_set'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(50)) # Field Location of the imported content set (Country)
    exproted_on = db.Column(db.Date()) # When was the content set exported from the library
    imported_on = db.Column(db.Date()) # automatically generated 
    imported_by = db.Column(db.Integer, db.ForeignKey('user.id')) # the name of user who imported the content set 
    lib_version = db.Column(db.String(20)) # Library version 
    content = db.relationship("Content", cascade="all, delete")
  
    def __init__(self, location, exported_on, imported_on ,lib_version, imported_by):
        self.location = location
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
    user_ids = db.relationship(ContentSet, backref='user', lazy = 'select' , uselist = False)
    

    def __init__(self,fullname,username,password):
        self.fullname = fullname
        self.username = username
        self.password = password        

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



object1 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="downloads", browser="chrome", device_type="desktop", device_os="windows")
object2 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="desktop", browser="safari", device_type="phone", device_os="ios")
object3 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="downloads", browser="safari", device_type="phone", device_os="ios")
object4 = Content(title="learn", language="spanish", content_type="pdf", subject="education", parent_folder="downloads", browser="safari", device_type="phone", device_os="android")
object5 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="desktop", browser="chrome", device_type="phone", device_os="android")
object6 = Content(title="learn", language="spanish", content_type="mp4", subject="education", parent_folder="downloads", browser="mozilla", device_type="phone", device_os="android")
object7 = Content(title="body parts", language="eng", content_type="mp4", subject="science", parent_folder="downloads", browser="moilla", device_type="phone", device_os="android")
object8 = Content(title="body parts", language="eng", content_type="mp4", subject="science", parent_folder="downloads", browser="chrome", device_type="phone", device_os="ios")
object9 = Content(title="stories", language="spanish", content_type="pdf", subject="education", parent_folder="desktop", browser="mozilla", device_type="phone", device_os="ios")
object10 = Content(title="stories", language="spanish", content_type="pdf", subject="education", parent_folder="downloads", browser="chrome", device_type="desktop", device_os="windows")
object11 = Content(title="stories", language="eng", content_type="mp4", subject="education", parent_folder="downloads", browser="mozilla", device_type="desktop", device_os="windows")
object12 = Content(title="stories", language="spanish", content_type="pdf", subject="education", parent_folder="folder C", browser="chrome", device_type="desktop", device_os="windows")
object13 = Content(title="body parts", language="eng", content_type="mp4", subject="science", parent_folder="downloads", browser="chrome", device_type="desktop", device_os="windows")
object14 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="downloads", browser="chrome", device_type="desktop", device_os="mac")
object15 = Content(title="learn", language="eng", content_type="pdf", subject="education", parent_folder="folder C", browser="mozilla", device_type="desktop", device_os="mac")
object16 = Content(title="body parts", language="eng", content_type="mp4", subject="science", parent_folder="folder C", browser="chrome", device_type="desktop", device_os="windows")
object17 = Content(title="algebra", language="eng", content_type="pdf", subject="education", parent_folder="downloads", browser="mozilla", device_type="phone", device_os="ios")
object18 = Content(title="algebra", language="eng", content_type="mp4", subject="education", parent_folder="folder C", browser="mozilla", device_type="phone", device_os="android")
object19 = Content(title="algebra", language="spanish", content_type="pdf", subject="education", parent_folder="folder C", browser="chrome", device_type="phone", device_os="ios")
object20 = Content(title="body parts", language="eng", content_type="mp4", subject="science", parent_folder="downloads", browser="chrome", device_type="phone", device_os="android")
db.session.add(object1)
db.session.add(object2)
db.session.add(object3)
db.session.add(object4)
db.session.add(object5)
db.session.add(object6)
db.session.add(object7)
db.session.add(object8)
db.session.add(object9)
db.session.add(object10)
db.session.add(object11)
db.session.add(object12)
db.session.add(object13)
db.session.add(object14)
db.session.add(object15)
db.session.add(object16)
db.session.add(object17)
db.session.add(object18)
db.session.add(object19)
db.session.add(object20)
db.session.commit()