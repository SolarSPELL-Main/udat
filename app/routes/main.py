from flask import Blueprint, render_template, url_for
from flask_login import login_user,current_user

main= Blueprint('main', __name__, url_prefix='/')


@main.route('/home/', methods=['GET', 'POST'])
def show():
    if current_user.is_authenticated:
       return render_template("home.html", title='home')
    else:
       return render_template("user_login.html", title='login')



