from flask import Blueprint, render_template,request
from flask_login import current_user
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import output_file
import sqlite3 as sql
import pandas as pd
from collections import Counter

content= Blueprint('content', __name__, url_prefix='/')
@content.route('/analysis', methods=['POST','GET'])
def plot():
   if current_user.is_authenticated:
        if request.method == 'POST':
            output_file("analysis.html") # plot output file
            conn = sql.connect('udat.db') # connect to database
            curs = conn.cursor()
            selected_col = request.form['col'] #selected option from the analysis.html
            curs.execute("SELECT "+ selected_col +" FROM Content") # select all categories from Data table
            x = curs.fetchall() # returns selected option tuple
            x_df = pd.DataFrame(x, columns=[selected_col]) 
            x_list = x_df[selected_col].values.tolist()
            x_counter = Counter(x_list)
            x_list = list(x_counter) # convert  counter dictionary to list in order to plot x_range and x 
            counter_vals = x_counter.values() # get the number of times the elements appear store in dictionary
            vals_list = list(counter_vals)
            p = figure(x_range=x_list, plot_height=300, plot_width=500,
            toolbar_location="right", tools="pan,wheel_zoom,box_zoom,undo,redo,reset,save")
            p.vbar(x=x_list, top=vals_list, width=0.9) 
            # remove grids
            p.xgrid.grid_line_color = None
            p.y_range.start = 0
            script,div = components(p)
            kwargs = {'script':script, 'div':div}
            return render_template('analysis.html', **kwargs)
        return render_template('analysis.html')
        
