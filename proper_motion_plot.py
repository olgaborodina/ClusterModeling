#import math
import matplotlib.pyplot as plt
import numpy as np

#Variables
NUMSTRINGS=56230 #56230 #number of strings in input file. Should be replaced in the future
j=0 #variable for reading file. Should be replaced in the future
xlist = [] #array for PM in RA 
ylist = [] #array for PM in DEC
# line[10] is PM in RA 
# line[12] is PM in DEC

# opening result-file
#try:        
#    g=open('result.txt','w')
#except IOError:
#    print('Can not find your file')

# reading input file and making arrays PMs
with open('NGC2516_100m.tsv', 'r') as f:   #opening initial file
#with open('NGC2516_100m_selected.txt', 'r') as f: #opening selected file
    while  (j<NUMSTRINGS):
        line = f.readline().split(';')
        if (len(line)>15):
        #print(line[8])
            try:
                xlist.append(float(line[10]))
                ylist.append(float(line[12]))
            except ValueError:
                xlist.append(100)
                ylist.append(100)
            print(j)
            j=j+1
f.close()

#writing in result-file           
#for i in range(len(xlist)):           
#    g.write('%s %s' % (xlist[i], ylist[i]))
#    g.write('\n')            
   
# making plot
plt.scatter(xlist, ylist, s=0.5, c='black')
plt.ylabel('pm in DEC, mas/y')
plt.xlabel('pm in RA, mas/y')
plt.savefig('Proper motion.png', dpi=100)
#xticks = np.linspace(min(xlist), max(xlist), 10)
#yticks = np.linspace(min(ylist), max(ylist), 10)
#ax = plt.gca()
#ax.set_xticks(xticks)
#ax.set_yticks(yticks)

plt.show()

#g.close()
