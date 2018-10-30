# script makes four kinds of plots: parallax (G), proper motion (G) in two 
# coordinates: RA and DEC, and also Color index - Magnitude Diagram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

in_file =input("Input the name of your file")
mode = input("Write 'p' for parallax plot, 'a' for proper motion plot in RA, 'd' for proper motion plot in DEC and 'c' for CMD")

def get_parameters(mode): 
    if (mode == 'p'):
        return 15,8,'G, mag','parallax, mas','parallax_plot'
    elif (mode == 'a'):
        return 15,10,'G, mag','pm in RA, mas/y','pm_inRA_plot'
    elif (mode == 'd'):
        return 15,12,'G, mag','pm in DEC, mas/y','pm_inDEC_plot'
    elif (mode == 'c'):
        return 21,15,'BP-RP, mag','G, mag','CMD_plot'
    else:
        raise ValueError 

Numx, Numy, x_name, y_name, name = get_parameters(mode)

data = pd.read_csv(f"{in_file}", delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)

data = data.apply(pd.to_numeric, errors='coerce') 

# making plot
fig, ax = plt.subplots(figsize=(16, 14)) #16:14 is size ratio 

ax.scatter(data[x_name], data[y_name], s=8, facecolor='white', edgecolor='black') 
ax.grid(c='#aaaaaa', ls='--')
if (mode != 'c'):        
    ax.set_ylim(-15, 15)      #cutting area for plot
if (mode == 'c'):
    locs, labels = plt.yticks()
    locs, labels = plt.xticks()
    plt.yticks(np.arange(2, 24, step=1.0))
    ax.invert_yaxis()
    plt.xticks(np.arange(-2, 5, step=0.5))

plt.xlabel(f"{x_name}")
plt.ylabel(f"{y_name}")

# define the name of input file
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}.png"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}.png"
    
plt.savefig(out_file, dpi=200)