# script makes three kinds of star selection, depending on: parallax,
# proper motion in two coordinates: RA and DEC.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

in_file =input("Input the name of your file")
mode= input("Write 'p' for parallax selection, 'a' for proper motion selection in RA, 'd' for proper motion selection in DEC")
per_cent =0.8 # quantile for errors distribution

def get_parameters(mode): 
    if (mode == 'p'):
        return 15,8,9,'G, mag','parallax, mas','error_par','parallax',0.2
    elif (mode == 'a'):
        return 15,10,11,'G, mag','pm in RA, mas/y','error_pminRA','pm_inRA',1.5
    elif (mode == 'd'):
        return 15,12,13,'G, mag','pm in DEC, mas/y','error_pminDEC','pm_inDEC', 1.5

    else:
        raise ValueError # what`s name of this Error?

Numx, Numy, NumErr, x_name,y_name, err_name, name, delt = get_parameters(mode)

# define the name of input file
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_selected_{name}_{delt}.txt"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}_{delt}.txt"    

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name, NumErr: err_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')


# cluster search
data['bin'] = pd.cut(bins=np.linspace(-15, 15, 1000), x=data[y_name]) #splitting interval

data['weight'] = np.exp(-data[x_name])
dist = data.groupby('bin')[['weight']].sum()
dist['average Gmag'] = dist.index.map(lambda x: x.right).astype(float)

fig, ax = plt.subplots(figsize=(16, 9))
dist.plot(x='average Gmag', y='weight', ax=ax, c='black')
ax.grid(c='#aaaaaa', ls='--')
plt.show()
        
print(dist['weight'].idxmax())
mid_value=dist['weight'].idxmax().mid #most likely value of parallax or proper motion for Cluster

#making an array of interval values

data['err_bin'] = pd.cut(bins=np.linspace(0, data[x_name].max(), 100), x=data[x_name])  # splitting interval
intervals = data.groupby('err_bin').apply(lambda df: df[err_name].quantile(per_cent))
intervals.index = intervals.index.map(lambda x: x.mid)
intervals.dropna(inplace=True)

def f(x, a, b):
    return np.exp(x) * a + b

popt, pcov = curve_fit(f, np.array(intervals.index.tolist()), np.array(intervals.tolist()))

delta_vec = f(data['G, mag'], *popt) + delt

#selection           
mask = (mid_value - delta_vec < data[y_name]) & (data[y_name] < mid_value + delta_vec)
data.loc[mask].to_csv(out_file, sep=';',header= False, index=False)

print ('I`ve worked so much, bring me some coffee')