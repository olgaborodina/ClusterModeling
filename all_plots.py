# script makes three kinds of star selection, depending on: parallax,
# proper motion in two coordinates: RA and DEC. 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#Variables
xlist = [] #array for x
ylist = [] #array for y

InFile =input("Input the name of your file")
mode = input("Write 'p' for parallax plot, 'a' for proper motion plot in RA, 'd' for proper motion plot in DEC and 'c' for CMD")

def get_parameters(mode): 
    if (mode == 'p'):
        return 15,8,'G, mag','parallax, mas','par_plot'
    elif (mode == 'a'):
        return 15,10,'G, mag','pm in RA, mas/y','pminRA_plot'
    elif (mode == 'd'):
        return 15,12,'G, mag','pm in DEC, mas/y','pminDEC_plot'
    elif (mode == 'c'):
        return 21,15,'BP-RP, mag','G, mag','CMD_plot'
    else:
        raise ValueError # what`s name of this Error?

Nx, Ny, xl, yl, name = get_parameters(mode)

data = pd.read_csv(f"{InFile}", delimiter=';', header=None)
data.rename(columns = {Nx : xl, Ny : yl}, inplace=True)

data[xl] = pd.to_numeric(data[xl],errors='coerce')
data[yl] = pd.to_numeric(data[yl],errors='coerce')

# making plot
fig, ax = plt.subplots(figsize=(16, 14)) #16:14 is szi==ize ratio 

ax.scatter(data[xl], data[yl], s=8, facecolor='white', edgecolor='black') 
ax.grid(c='#aaaaaa', ls='--')
if (mode != 'c'):        
    ax.set_ylim(-15, 15)      #cutting area for plot
if (mode == 'c'): 
    ax.invert_yaxis() 
plt.xlabel(f"{xl}")
plt.ylabel(f"{yl}")
plt.savefig(f"{name}.png", dpi=200)