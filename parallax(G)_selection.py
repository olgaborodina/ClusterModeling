#Variables
NUMSTRINGS=56230 #number of strings in input file. Should be replaced in the future
j=0 #variable for reading file. Should be replaced in the future
dPar=0.5 # interval for parallax-selection
# opening result-file
try:        
    g=open('NGC2516_100m_selected.txt','w')
except IOError:
    print('Can not find your file')

# reading input file and select non-cluster stars
with open('NGC2516_100m.tsv', 'r') as f:
    while  (j<NUMSTRINGS):       
        line = f.readline()
        star=line.split(';')
        if (len(star)>15):
            if (float(star[15])<18):
                try:
                    if abs(float(star[8])-2.5)>dPar:                    
                        print('too far')
                    else: 
                        g.write(line)
                        print(j)
                except ValueError:
                    print('aaaaaa')
            else:
                try:
                    if abs(float(star[8])-2.5)>(dPar+(float(star[15])-18)*0.65):                    
                        print('too far___')
                    else: 
                        g.write(line)
                        print(j)
                except ValueError:
                    print('aaaaaa___')               
        j=j+1
f.close()
g.close()
print ('I`ve worked so much, bring me some coffee')