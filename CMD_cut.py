# script makes three kinds of star selection, depending on: parallax,
# proper motion in two coordinates: RA and DEC.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

in_file =input("Input the name of your file")

Numx, Numy, x_name,y_name, name= 21, 15, 'BP-RP, mag','G, mag','CMD_cutted'

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')

# trying to find turning spot on CMD
def f(x, a, b, c, d):
    return a * x * x * x + b * x * x + c * x + d

#_array is a frame for making approximation of unfiltered main sequence 
_array = data.dropna(subset=['BP-RP, mag']).loc[data.dropna(subset=['BP-RP, mag'])['G, mag'] > 14]
popt, pcov = curve_fit(f, _array['G, mag'], _array['BP-RP, mag'])

#selection
G_limit = _array['G, mag'].loc[f(_array['G, mag'], *popt).idxmax()]           
mask = (G_limit > data[y_name])

# define the name of input file
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_{name}_{G_limit}.txt"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}_{G_limit}.txt"  
    

data=data.loc[mask]
#data.loc[mask].to_csv(out_file, sep=';', header= False, index=False)



data.to_csv(out_file, sep=';', header= False, index=False)

print ('I`ve worked so much, bring me some coffee')