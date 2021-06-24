from flask import Blueprint, render_template, url_for


main= Blueprint('main', __name__, url_prefix='/')


@main.route('/home/', methods=['GET', 'POST'])
def show():
    return render_template("home.html", title='home')


