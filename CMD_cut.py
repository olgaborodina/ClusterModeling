# script makes three kinds of star selection, depending on: parallax,
# proper motion in two coordinates: RA and DEC.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

in_file =input("Input the name of your file")

Numx, Numy, x_name,y_name, name, MAG_limit= 21, 15, 'BP-RP, mag','G, mag','CMD_cutted', 19

# define the name of input file
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}_{MAG_limit}.txt"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}_{MAG_limit}.txt"    

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')


#selection           
mask = (MAG_limit > data[y_name])
data.loc[mask].to_csv(out_file, sep=';', header= False, index=False)

print ('I`ve worked so much, bring me some coffee')