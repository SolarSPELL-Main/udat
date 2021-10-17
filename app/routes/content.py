from bokeh.models.annotations import Title
from bokeh.models.sources import ColumnDataSource, ColumnarDataSource
from bokeh.models.widgets.tables import DataTable, TableColumn
from flask.helpers import flash, url_for
from sqlalchemy.sql.expression import join, table

from sqlalchemy.sql import text
from werkzeug.utils import redirect
from app.models import Content, ContentSet, Country, Location
from flask import Blueprint, render_template,request
from flask_login import current_user
from app import db
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import output_file
import pandas as pd
from collections import Counter
from flask_paginate import Pagination, get_page_parameter


saved_queries = []
content= Blueprint('content', __name__, url_prefix='/content')
def get_lists():
    language = db.session.query(Content.language).group_by("language").all()
    content_type = db.session.query(Content.content_type).group_by("content_type").all()
    subject = db.session.query(Content.subject).group_by("subject").all()
    parent_folder = db.session.query(Content.parent_folder).group_by("parent_folder").all()
    browser = db.session.query(Content.browser).group_by("browser").all() 
    device_type = db.session.query(Content.device_type).group_by("device_type").all()
    device_os = db.session.query(Content.device_os).group_by("device_os").all()
    version = db.session.query(ContentSet.lib_version).group_by("lib_version").all()
    location = db.session.query(Location.name).group_by("name").all()
    country = db.session.query(Country.name).group_by("name").all()
    return(language,content_type,subject,parent_folder,browser,device_type,device_os,version,location,country)
def selected():
    selected_col = request.form.get('col') #selected option from the analysis.html
    selected_lang = request.form.get('lang')
    selected_conType = request.form.get('con_type')
    selected_subject = request.form.get('subject')
    selected_parentFolder = request.form.get('parent_folder')
    selected_browser = request.form.get('browser')
    selected_deviceType = request.form.get('device_type')
    selected_deviceOS = request.form.get('device_os')
    selected_version = request.form.get('lib_version')
    selected_location = request.form.get('location')
    selected_country = request.form.get('country')
    filters_used = []
    queries = []
    if selected_lang != "Language":
        queries.append(Content.language==selected_lang)
        filters_used.append("Language("+selected_lang+")")
    if selected_conType != "content_type":
        queries.append(Content.content_type==selected_conType)
        filters_used.append("Content Type("+selected_conType+")")
    if selected_subject != "subject" :
        queries.append(Content.subject==selected_subject)
        filters_used.append("Subject(" + selected_subject+")")
    if selected_parentFolder != "parent_folder":
        queries.append(Content.parent_folder==selected_parentFolder)
        filters_used.append("Parent Folder("+selected_parentFolder+")")
    if selected_browser != "browser":
        queries.append(Content.browser==selected_browser)
        filters_used.append("Browser("+selected_browser+")")
    if selected_deviceType != "device_type":
        queries.append(Content.device_type==selected_deviceType)
        filters_used.append("Device Type("+selected_deviceType+")")
    if selected_deviceOS != "device_os":
        queries.append(Content.device_os==selected_deviceOS)
        filters_used.append("Device Operating System("+selected_deviceOS+")")
    if selected_version !="lib_version":
        queries.append(ContentSet.lib_version==selected_version)
        filters_used.append("Version("+selected_version+")")
    if selected_location != "location":
        queries.append(Location.name==selected_location)
        filters_used.append("Location("+selected_location+")")
    if selected_country != "country":
        queries.append(Country.name==selected_country)
        filters_used.append("Country("+selected_country+")") 
    global saved_queries  
    saved_queries = queries
    return queries,selected_col, filters_used

@content.route('/analysis', methods=['POST','GET'])
def show():
    language,content_type,subject,parent_folder,browser,device_type,device_os,version,location,country= get_lists()
    return render_template('analysis.html',language=language,
                                        content_type = content_type, subject = subject,
                                        parent_folder = parent_folder, browser = browser,
                                        device_type = device_type,
                                      device_os = device_os, version=version, location=location,country=country)


@content.route('/results/', methods=['POST','GET'])
def plot():
   if current_user.is_authenticated:
        if request.method == 'POST':
            queries,selected_col, filters_used = selected()
            output_file("plot.html") # plot output file
            x = db.session.query(getattr(Content,selected_col)). join(ContentSet,ContentSet.id == Content.set_id).\
                                            join(Location,Location.id == ContentSet.location ).\
                                            join(Country,Country.id == Location.country_id).\
                                            filter(*queries).all()
            if x == []:
                flash('No data available with the selected filters')
            else:
                if request.form['submit_button'] == 'plot':
                    # select all categories from Content table
                    x_df = pd.DataFrame(x, columns=[selected_col]) 
                    x_list = x_df[selected_col].values.tolist()
                    x_counter = Counter(x_list)
                    x_list = list(x_counter) # convert  counter dictionary to list in order to plot x_range and x 
                    counter_vals = x_counter.values() # get the number of times the elements appear store in dictionary
                    vals_list = list(counter_vals)
                    p = figure(x_range = x_list, plot_height=300, plot_width=500,
                                toolbar_location="right", 
                                tools="pan,wheel_zoom,box_zoom,undo,redo,reset,save")
                    p.vbar(x = x_list, top=vals_list, width=0.9) 
                    # remove grids
                    p.xgrid.grid_line_color = None
                    p.y_range.start = 0
                    title = '\n'.join(filters_used)
                    
                    script,div = components(p)
                    kwargs = {'script':script, 'div':div}
                    return render_template('plot.html', **kwargs, filters=title, selected_col = selected_col)
                else:
                    y = db.session.query(Content,ContentSet,Location,Country).join(ContentSet,ContentSet.id == Content.set_id).\
                                         join(Location,Location.id == ContentSet.location ).\
                                         join(Country,Country.id == Location.country_id).\
                                         filter(*queries).paginate(page=1, per_page=50,error_out=True)
                    return render_template('show_list.html',y=y)
            return redirect(url_for('content.show'))
        
   else:
     return render_template("user_login.html", title='login')
@content.route('/table/<int:page_num>', methods=['POST','GET'])
def table(page_num):
    if request.method =='GET':
            queries1 = saved_queries
            y = db.session.query(Content,ContentSet,Location,Country).join(ContentSet,ContentSet.id == Content.set_id).\
                                                            join(Location,Location.id == ContentSet.location ).\
                                                            join(Country,Country.id == Location.country_id).\
                                                            filter(*queries1).paginate(per_page=50,page=page_num,error_out=True)
            return render_template('show_list.html',y=y)  