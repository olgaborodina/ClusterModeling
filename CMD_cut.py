# script for deleting the rest of non-cluster stars by cutting
# faint stars and also by choosing some manually

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from bokeh.plotting import figure, show, ColumnDataSource, output_file
from bokeh.models import HoverTool

in_file =input("Input the name of your file")
#in_file='NGC2516_100m_selected_parallax_0.2_pm_inRA_1.5_pm_inDEC_1.5.txt'

Numx, Numy, x_name,y_name, name= 21, 15, 'BP-RP, mag','G, mag','CMD_cutted'

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')


to_cut = input("'m' to choose a limit manually and 'a' to define a limit automatically")

if to_cut == 'm':
    G_limit = float(input("G_limit"))
if to_cut == 'a':
    
    # trying to find turning spot on CMD
    def f(x, a, b, c, d):
        return a * x * x * x + b * x * x + c * x + d

    #_array is a frame for making approximation of unfiltered main sequence 
    _array = data.dropna(subset=['BP-RP, mag']).loc[data.dropna(subset=['BP-RP, mag'])['G, mag'] > 14]
    popt, pcov = curve_fit(f, _array['G, mag'], _array['BP-RP, mag'])

    #selection by magnitude limit
    G_limit = _array['G, mag'].loc[f(_array['G, mag'], *popt).idxmax()]           
mask = (G_limit > data[y_name])
data=data.loc[mask]

# rename indexes for rows
data.index = pd.RangeIndex(len(data.index))

# function for making CMD using one data
def plot_CMD (data):
    source = ColumnDataSource(
            data=dict(
                x=data[x_name],
                y=data[y_name],
            )
        )
    hover = HoverTool(
            tooltips=[
                ("index", "$index"),
                ("(x,y)", "($x, $y)"),
            ]
        )
    output_file('CMD.html')
    p = figure(plot_width=800, plot_height=800, tools=[hover],x_range = (-0.5, 3.5), y_range = (19, 4))
    p.circle('x', 'y', size=4, source=source, color = "black", alpha = 0.75)
    return show(p)

plot_CMD(data)

# changing data manually! too risky!
command = 'continue'

while command == 'continue':
    to_do, index = input("1. 'd' to delete star, 's 0 ' to stop,'a' for again Bokeh plot, 'r' to return previous data 2. index of star").split(' ')
    index = int(index)
    if to_do == 'd':    
        data_saved = data
        data = data.drop(index)
        data.index = pd.RangeIndex(len(data.index))
    if to_do == 'r':
         data = data_saved          
    if to_do == 's':
        command = 'stop'
    if to_do == 'a':
        plot_CMD(data)
        
# define the name of input file and write there
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}_{G_limit}.txt"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}_{G_limit}.txt"  
data.to_csv(out_file, sep=';', header= False, index=False)

print ('I`ve worked so much, bring me some coffee')