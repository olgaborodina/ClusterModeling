import pandas as pd
import numpy as np


InFile =input("Input the name of your file")
ch = input("Write 'p' for parallax plot, 'a' for proper motion plot in RA, 'd' for proper motion plot in DEC")

if (ch == 'p'):
    Nx=15                   # Number in initial array for х
    Ny=8                    # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='parallax, mas'      # Name for y-axis
    name='par'              # Name for plot
    delt=0.3                # interval for parallax-selection
    tgA=0.75                # angle of the "error`s wings"
   
elif (ch == 'a'):
    Nx=15                   # Number in initial array for  х
    Ny=10                   # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='pm in RA, mas/y'    # Name for y-axis
    name='pminRA_plot'      # Name for plot
    delt=0.3                # interval for parallax-selection
    tgA=0                   # angle of the "error`s wings"

elif (ch == 'd'):
    Nx=15                   # Number in initial array for  х
    Ny=12                   # Number in initial array for  у
    xl='G, mag'             # Name for x-axis
    yl='pm in DEC, mas/y'   # Name for y-axis
    name='pminDEC_plot'     # Name for plot
    delt=0.3                # interval for parallax-selection
    tgA=0                   # angle of the "error`s wings"    
    
# opening result-file
try:        
    g=open(f"NGC2516_100m_selected_{name}_{delt}_{tgA}.txt",'w')
except IOError:
    print('Can not find your file')
    
# reading input file  
data = pd.read_csv(f"{InFile}", delimiter=';', header=None)
data = data.iloc[:, [Ny, Nx]]                                   # need to read about it
data[Nx] = data[Nx].replace('          ', np.nan).astype(float) 
data[Ny] = data[Ny].replace('          ', np.nan).astype(float) 

# and select non-cluster stars                                  # write it!!!


g.close()
print ('I`ve worked so much, bring me some coffee')             # you have not deserve it yet

