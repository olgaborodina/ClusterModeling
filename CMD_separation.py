# script for separation the stars into binaries and single stars

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
from bokeh.plotting import figure, show, ColumnDataSource, output_file
from bokeh.models import HoverTool

Numx, Numy, x_name,y_name, name= 21, 15, 'BP-RP, mag','G, mag','CMD_separated'

#reading inputs
def reading(file):
    data = pd.read_csv(file, delimiter=';', header=None)
    data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    data.index = pd.RangeIndex(len(data.index))
    return data

que=input("Do you want to work with a new file? 'y' or 'n'")
if que == 'y':
    f = input("Input the name of your file")
    data_singles = reading(f)    
    data_binaries = pd.DataFrame()
if que == 'n':
    f_s = input("Input the name of your file with single stars")
    f_b = input("Input the name of your file with binary stars")
    data_singles = reading(f_s)    
    data_binaries = reading (f_b)
    f = f_s.split('_CMD_separated_singles')[0] + f_s.split('_CMD_separated_singles')[1]
    
# function for making CMD 
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
    p = figure(plot_width=900, plot_height=900, tools=[hover],x_range = (-0.5, 3.5), y_range = (19, 4))
    p.circle('x', 'y', size=3, source=source, color = "black", alpha = 0.75)
    return show(p)

plot_CMD(data_singles)

# changing data manually! too risky!
command = 'continue'

while command == 'continue':
    to_do, index = input("1. 'b' for separation binary, 's 0' for stop, 'r' for returning previous data 2. index of star").split(' ')
    index = int(index)
    if to_do == 'b':
        data_saved_b = data_binaries
        data_saved_s = data_singles
        
        data_binaries = data_binaries.append(data_singles.loc[index])
        data_binaries = data_binaries[data_singles.columns]
        data_singles = data_singles.drop(index)
        data_singles.index = pd.RangeIndex(len(data_singles.index))
        data_binaries.index = pd.RangeIndex(len(data_binaries.index))
        
        fig, ax = plt.subplots(figsize=(16, 14)) #16:14 is size ratio 
        ax.scatter(data_binaries[x_name], data_binaries[y_name], s=8, c='red')
        ax.scatter(data_singles[x_name], data_singles[y_name], s=8, facecolor='white', edgecolor='black') 
        ax.grid(c='#aaaaaa', ls='--')
        locs, labels = plt.yticks()
        locs, labels = plt.xticks()
        plt.yticks(np.arange(4, 19, step=1.0))
        ax.invert_yaxis()
        plt.xticks(np.arange(-0.5, 4, step=0.5))
        plt.xlabel(f"{x_name}")
        plt.ylabel(f"{y_name}")
        plot_CMD(data_singles)
    if to_do == 'r':
         data_singles = data_saved_s
         data_binaries = data_saved_b
    if to_do == 's':
        command = 'stop'
        
# output files
data_singles.to_csv(f"{f.split('.txt')[0]}_{name}_singles.txt", sep=';', header= False, index=False)
data_binaries.to_csv(f"{f.split('.txt')[0]}_{name}_binaries.txt"  , sep=';', header= False, index=False)
plt.savefig(f"{f.split('.txt')[0]}_{name}_plot.png", dpi=200)

print ('I`ve worked so much, I deserve a chocolate bar! pleeeease!')