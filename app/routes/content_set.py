from flask import Blueprint, render_template
from app.models import Content, ContentSet
content_set= Blueprint('content_set', __name__, url_prefix='/content_set')

# This is where the routes and their defenitions will go 
