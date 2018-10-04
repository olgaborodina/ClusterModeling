# script makes four kinds of plots: parallax (G), proper motion (G) in two 
# coordinates: RA and DEC, and also Color index - Magnitude Diagram
import matplotlib.pyplot as plt
import numpy as np

#Variables
xlist = [] #array for x
ylist = [] #array for y

InFile =input("Input the name of your file")
ch = input("Write 'p' for parallax plot, 'a' for proper motion plot in RA, 'd' for proper motion plot in DEC and 'c' for CMD")


if (ch == 'p'):
    Nx=15                   # Number in initial array for х
    Ny=8                    # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='parallax, mas'      # Name for y-axis
    name='parallax_plot'    # Name for plot
   
elif (ch == 'a'):
    Nx=15                   # Number in initial array for  х
    Ny=10                   # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='pm in RA, mas/y'    # Name for y-axis
    name='pminRA_plot'      # Name for plot
    
elif (ch == 'd'):
    Nx=15                   # Number in initial array for  х
    Ny=12                   # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='pm in DEC, mas/y'   # Name for y-axis
    name='pminDEC_plot'     # Name for plot
        
    
elif (ch == 'c'):
    Nx=21                   # Number in initial array for  х
    Ny=15                   # Number in initial array for  у
    xl='BP-RP, mag'         # Name for x-axis
    yl='G, mag'             # Name for y-axis
    name='CMD_plot'         # Name for plot
else:
    print('Error "please check your input letter and try again"')

def get_float(st): #function for getting float from string
    try:
        return float(st)
    except ValueError:
        return None
    
with open(f"{InFile}", 'r') as f:  #reading file and making arrays 
    lines = f.readlines()
xlist = [line.split(';')[Nx] for line in lines]
ylist = [line.split(';')[Ny] for line in lines]
f.close()

x = [get_float(elem) for elem in xlist]
y = [get_float(elem) for elem in ylist]

# making plot
fig, ax = plt.subplots(figsize=(16, 14)) #16:14 is szi==ize ratio 

ax.scatter(x, y, s=8, facecolor='white', edgecolor='black') 
ax.grid(c='#aaaaaa', ls='--')
if (ch != 'c'):        
    ax.set_ylim(-15, 15)      #cutting area for plot
if (ch == 'c'): 
    ax.invert_yaxis() 
plt.xlabel(f"{xl}")
plt.ylabel(f"{yl}")
plt.savefig(f"{name}.png", dpi=200)


