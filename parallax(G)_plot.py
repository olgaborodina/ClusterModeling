#import math
import matplotlib.pyplot as plt
import numpy as np

#Variables
NUMSTRINGS=56230 #number of strings in input file. Should be replaced in the future
j=0 #variable for reading file. Should be replaced in the future
xlist = [] #array for G, mag
ylist = [] #array for parallax, mas

# opening result-file
try:        
    g=open('result.txt','w')
except IOError:
    print('Can not find your file')

# reading input file and making arrays of Gmag and parallax
with open('NGC2516_100m.tsv', 'r') as f:
    while  (j<NUMSTRINGS):
        line = f.readline().split(';')
        if (len(line)>15):
        #print(line[8])
            try:
                if float(line[8])>20:
                    ylist.append(0)
                else:
                    ylist.append(float(line[8]))
            except ValueError:
                ylist.append(0)
            xlist.append(float(line[15]))
            print(j)
            j=j+1
f.close()

#writing in result-file           
#for i in range(len(xlist)):           
#    g.write('%s %s' % (xlist[i], ylist[i]))
#    g.write('\n')            
   
# making plot
plt.scatter(xlist, ylist, s=1, c='black')
plt.ylabel('parallax, mas')
plt.xlabel('G, mag')
plt.savefig('parallax.png', dpi=100)
#xticks = np.linspace(min(xlist), max(xlist), 10)
#yticks = np.linspace(min(ylist), max(ylist), 10)
#ax = plt.gca()
#ax.set_xticks(xticks)
#ax.set_yticks(yticks)

plt.show()

g.close()
