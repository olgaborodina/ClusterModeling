
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m
from scipy.interpolate import interp1d
import scipy.optimize
from random import random

def to_mf (a, b, c): #gets mass of star with definite magnitude
    func = interp1d(a, b)
    return func(c)

def neyman(data_1, data_2): #gets q randomly from definite distribution
    iter = True
    while iter == True:
        x, yr = random()*data_1.max(), random()
        y = interp1d(data_1, data_2)
        if x >= data_1.min() and yr <= y(x):
            iter = False
            return x
        else:
            iter = True

def make_cluster (data, mf): # makes a model of cluster in data with definite mass function
    arr = []
    for  i in range (0, len(data)):
        arr.append(neyman(mf['Mass'], mf['MF']))
    return pd.DataFrame(data = {'Mass' : arr})

#input files
iso = pd.read_csv("NGC2516_isochrone_1.2e8.txt", delimiter=' ')
mf = pd.read_csv("NGC2516_Mass_function.txt", delimiter=';')
infile_q = "func_gr.txt"
data_q = pd.read_csv(infile_q, delimiter=' ', header=None, names = ['q','F'])

Numx, Numy, x_name,y_name= 21, 15, 'BP-RP, mag','G, mag'
data_singles = pd.read_csv("NGC2516_100m_selected_parallax_0.2_pm_inRA_1.5_pm_inDEC_1.5_CMD_cutted_18_CMD_separated_singles.txt", delimiter=';', header = None)
data_binaries = pd.read_csv("NGC2516_100m_selected_parallax_0.2_pm_inRA_1.5_pm_inDEC_1.5_CMD_cutted_18_CMD_separated_binaries.txt", delimiter=';', header = None)
data_singles.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data_binaries.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)

# try to make a mean value 
mask =(1.215 <data_singles['BP-RP, mag']) & (data_singles['BP-RP, mag']<1.22)
err_mag = (data_singles['G, mag'].loc[mask].max() -  data_singles['G, mag'].loc[mask].min())/2

#making single stars in cluster
cluster = make_cluster(data_singles, mf)
cluster['G, mag'] = to_mf(iso['Mass'], iso['Gmag'], cluster['Mass'])
cluster['BP-RP, mag'] = to_mf(iso['Mass'], iso["G_BPmag"], cluster['Mass']) - to_mf(iso['Mass'], iso["G_RPmag"], cluster['Mass']) 
cluster['G, mag'] += np.random.normal(loc=0.0, scale=err_mag, size=len(cluster['G, mag']))

fig, ax = plt.subplots(figsize = (9, 7))
ax.hist(cluster['Mass'], bins=80, color = 'gray')
plt.show()

#making binary stars in cluster
binaries = make_cluster(data_binaries, mf)
binaries.columns=['Mass1']
binaries['Mass2'] = binaries['Mass1'] * np.fromiter((neyman(data_q['q'], data_q['F']) for x in range(len(binaries))), float)
binaries['Mass2'][binaries['Mass2'] < iso['Mass'].min()] = iso['Mass'].min()

binaries['G1, mag'] = to_mf(iso['Mass'], iso['Gmag'], binaries['Mass1'])
binaries['BP1, mag'] = to_mf(iso['Mass'], iso["G_BPmag"],  binaries['Mass1'])
binaries['RP1, mag'] = to_mf(iso['Mass'], iso["G_RPmag"],  binaries['Mass1'])

binaries['G2, mag'] = to_mf(iso['Mass'], iso['Gmag'], binaries['Mass2'])
binaries['BP2, mag'] = to_mf(iso['Mass'], iso["G_BPmag"],  binaries['Mass2'])
binaries['RP2, mag'] = to_mf(iso['Mass'], iso["G_RPmag"],  binaries['Mass2'])

binaries['G, mag'] = binaries['G2, mag'] - 2.5 *np.log10(1+ pow(2.512, binaries['G2, mag'] - binaries['G1, mag']))
binaries['BP-RP, mag'] = binaries['BP2, mag'] - 2.5 *np.log10(1+ pow(2.512, binaries['BP2, mag'] - binaries['BP1, mag'])) - (binaries['RP2, mag'] - 2.5 *np.log10(1+ pow(2.512, binaries['RP2, mag'] - binaries['RP1, mag'])))

#making plot
fig, ax = plt.subplots(figsize=(16,14)) #16:14
ax.scatter (cluster['BP-RP, mag']  +3.1*0.13*(1.2 - 0.65) , cluster['G, mag'] + 5 * np.log10(410) - 5 + 3.1*0.13*0.86,facecolor='white', edgecolor='black', s = 8)
ax.scatter (binaries['BP-RP, mag']  +3.1*0.13*(1.2 - 0.65), binaries['G, mag']  + 5 * np.log10(410) - 5 + 3.1*0.13*0.86, c ='red', s = 8)
ax.invert_yaxis()
ax.grid(c='#aaaaaa', ls='--')
plt.xlabel('BP-RP, mag', size = 20)
plt.yticks(np.arange(6,19, step=1.0))
ax.tick_params(axis='both', which='major', labelsize=15)
plt.ylabel('G, mag', size = 20)
plt.savefig(f"NGC2516_model_{infile_q.split('.')[0]}.png", dpi=200)