# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 00:09:20 2018

Stock plotter interactive: plots the 1 week and 3 month variations of a set of stock indices

@Author: Pouya Rezazadeh Kalehbasti (Rezazadeh.Pouya@gmail.com)
"""





from iexfinance import get_historical_data as ghd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import BDay
import random
from bokeh.palettes import Plasma256
from bokeh.plotting import figure, output_file, show
# from scoop import futures

Measures = {} # dictionary of [1m, 3m, 1y, 5y] ROIs

Indices = ['AMRN','SQ','AMD','MED','TEAM','SODA','NVDA','AMZN','TECH','NFLX',
           'ADBE','SNE','INGN','AAPL']


## Date definitions
end = datetime.now().date()
start = end - relativedelta(months=3) - BDay()

## Main function: retrieve the data and find the desired measures
data_frames = ghd(Indices, start = start, end = end, output_format = 'pandas')


## Defining the date range
df = data_frames[Indices[0]]['open'] 
datelist = [datetime.strptime(df.index[x],'%Y-%m-%d') for x in range(len(df.index))]


p = figure(plot_width=1600, plot_height=800, x_axis_type="datetime")

# Create color palette
rand_nums = random.sample(range(1, 256), len(data_frames))
colors = [Plasma256[x] for x in rand_nums]

for ind, color in zip(Indices, colors):
    df = data_frames[ind]['open']
    df /= df[0] # Normalizing        
    
    p.line(datelist, list(df), line_width=2, legend=ind, color=color, alpha=0.8)

p.legend.location = "top_left"
p.legend.click_policy="hide"
output_file("interactive_legend.html", title="interactive_legend")
show(p)