# script makes four kinds of plots: parallax (G), proper motion (G) in two 
# coordinates: RA and DEC, and also Color index - Magnitude Diagram
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

In_File =input("Input the name of your file")
#In_File ='NGC2516_100m.tsv'
mode= input("Write 'p' for parallax selection, 'a' for proper motion selection in RA, 'd' for proper motion selection in DEC")

def get_parameters(mode): 
    if (mode == 'p'):
        return 15,8,'G, mag','parallax, mas','par',0.3,0.75
    elif (mode == 'a'):
        return 15,10,'G, mag','pm in RA, mas/y','pminRA',3,0.3
    elif (mode == 'd'):
        return 15,12,'G, mag','pm in DEC, mas/y','pminDEC',3,0.3
    else:
        raise ValueError # what`s name of this Error?

Nx, Ny, xl,yl, name, delt, tgA = get_parameters(mode)
    
# reading input file  and creating data-arrays
data = pd.read_csv(f"{In_File}", delimiter=';', header=None)
data.rename(columns = {Nx : xl, Ny : yl}, inplace=True)
pd.to_numeric(data[xl],errors='coerce')
pd.to_numeric(data[yl],errors='coerce')                          
#print (data.head())

# cluster search
data['bin'] = pd.cut(bins=np.linspace(-15, 15, 1000), x=data[yl]) #splitting interval

data['weight'] = np.exp(-data[xl])
dist = data.groupby('bin')[['weight']].sum()
dist['average Gmag'] = dist.index.map(lambda x: x.right).astype(float)

fig, ax = plt.subplots(figsize=(16, 9))
dist.plot(x='average Gmag', y='weight', ax=ax, c='black')
ax.grid(c='#aaaaaa', ls='--')
plt.show()
        
print(dist['weight'].idxmax())
mid_value=dist['weight'].idxmax().mid #most likely value of parallax or proper motion for Cluster

#print (data[xl])
#print (data.values[100][0])
x=data['G, mag']
delta_vec = pd.Series(len(x) * [np.nan])
delta_vec[x < 18] = delt 
delta_vec[x >= 18] = delt + (data['G, mag'] - 18) * tgA

def f(x, tgA):
    return delta_vec
    
delta = f(data['G, mag'], tgA)

#selection           
mask = (mid_value - delta < data[yl]) & (data[yl] < mid_value + delta)
data.loc[mask].to_csv(f"NGC2516_100m_selected_{name}_{delt}_{tgA}.txt", sep=';',header= False, index=False)

print ('I`ve worked so much, bring me some coffee')  # you have not deserved it yet

