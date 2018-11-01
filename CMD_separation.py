# script for separation the stars into binaries and singles

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from bokeh.plotting import figure, show, ColumnDataSource, output_file
from bokeh.models import HoverTool

#in_file =input("Input the name of your file")
in_file='NGC2516_100m_selected_parallax_0.2_pm_inRA_1.5_pm_inDEC_1.5_CMD_cutted_18.6811.txt'

Numx, Numy, x_name,y_name, name= 21, 15, 'BP-RP, mag','G, mag','CMD_separated'

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')

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
    p = figure(plot_width=600, plot_height=600, tools=[hover],x_range = (-0.5, 3.5), y_range = (19, 4))
    p.circle('x', 'y', size=4, source=source, color = "black", alpha = 0.75)
    return show(p)

plot_CMD(data)

# changing data manually! too risky!
data_binaries = pd.DataFrame()
data_binaries.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data_singles = data
command = 'continue'

while command == 'continue':
    to_do, index = input("1. 'b' for separation binary, 's' for stop, 'r' for returning previous data 2. index of star").split(' ')
    index = int(index)
    if to_do == 'b':
        data_saved_b = data_binaries
        data_saved_s = data_singles
        
        data_binaries.append(data.loc[index])
        data_singles = data.drop(index)
        data_singles.index = pd.RangeIndex(len(data_singles.index))
        data_binaries.index = pd.RangeIndex(len(data_binaries.index))
        
        fig, ax = plt.subplots(figsize=(16, 14)) #16:14 is size ratio 
        ax.scatter(data_binaries[x_name], data_binaries[y_name], s=8, c='red')
        ax.scatter(data_singles[x_name], data_singles[y_name], s=8, facecolor='white', edgecolor='black') 
        ax.grid(c='#aaaaaa', ls='--')
        locs, labels = plt.yticks()
        locs, labels = plt.xticks()
        plt.yticks(np.arange(2, 24, step=1.0))
        ax.invert_yaxis()
        plt.xticks(np.arange(-2, 5, step=0.5))
        plt.xlabel(f"{x_name}")
        plt.ylabel(f"{y_name}")
        
        plot_CMD(data_singles)
    if to_do == 'r':
         data_singles = data_saved_s
         data_binaries = data_saved_b
    if to_do == 's':
        command = 'stop'
        
# define the name of input file and write there
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file1 = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}_singles.txt"
    out_file2 = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}_binaries.txt"
else:
    out_file1 = f"{in_file.split('.txt')[0]}_{name}_singles.txt"
    out_file2 = f"{in_file.split('.txt')[0]}_{name}_binaries.txt"  
data_singles.to_csv(out_file1, sep=';', header= False, index=False)
data_binaries.to_csv(out_file2, sep=';', header= False, index=False)

print ('I`ve worked so much, bring me some coffee')