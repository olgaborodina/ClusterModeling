# script makes three kinds of star selection, depending on: parallax,
# proper motion in two coordinates: RA and DEC.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

in_file =input("Input the name of your file")
mode= input("Write 'p' for parallax selection, 'a' for proper motion selection in RA, 'd' for proper motion selection in DEC")

def get_parameters(mode): 
    if (mode == 'p'):
        return 15,8,'G, mag','parallax, mas','par',0.3,0.75
    elif (mode == 'a'):
        return 15,10,'G, mag','pm in RA, mas/y','pminRA',1.5,0.3
    elif (mode == 'd'):
        return 15,12,'G, mag','pm in DEC, mas/y','pminDEC',3,0.3
    else:
        raise ValueError # what`s name of this Error?

Numx, Numy, x_name,y_name, name, delt, tgA = get_parameters(mode)

# define the name of input file
par_name=in_file.split('_')
len (par_name)
if len(par_name) <= 2:
    out_file = f"{par_name[0]}_{par_name[1].split('.tsv')[0]}_selected_{name}_{delt}_{tgA}.txt"
else:
    out_file = f"{in_file.split('.txt')[0]}_{name}_{delt}_{tgA}.txt"    

# reading input file  and creating data-arrays
data = pd.read_csv(in_file, delimiter=';', header=None)
data.rename(columns = {Numx : x_name, Numy : y_name}, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')

#print (data.head())

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
x=data['G, mag']
delta_vec = pd.Series(len(x) * [np.nan])
delta_vec[x < 18] = delt 
delta_vec[x >= 18] = delt + (data['G, mag'] - 18) * tgA

def f(x, tgA):
    return delta_vec    
delta = f(data['G, mag'], tgA)

#selection           
mask = (mid_value - delta < data[y_name]) & (data[y_name] < mid_value + delta)
data.loc[mask].to_csv(out_file, sep=';',header= False, index=False)

print ('I`ve worked so much, bring me some coffee')