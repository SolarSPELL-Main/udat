from flask import Blueprint, render_template
from app.models import Content, ContentSet

main= Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=['GET', 'POST'])
@main.route('/home/', methods=['GET', 'POST'])
def show():
    return render_template("home.html")
