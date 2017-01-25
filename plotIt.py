import numpy as np
import pylab as pl

# Use numpy to load the data contained in the file
#data = np.loadtxt('/home/vijoy/deepwalk-master/karate.embeddings')
#data = np.loadtxt('onlydoc_noIndicators.embeddings')
data = np.loadtxt('onlydoc_with2indicators.embeddings')
#data = np.loadtxt('onlydoc.embeddings')
# plot the first column as x, and second column as y
c=[]
for i in data[:,0]:
  if i < 33:
    c.append('red')
  else:
  #  if i < 66:
  #    c.append('blue')
  #  else:
     c.append('green')
pl.scatter(data[:,1], data[:,2], s=50, c=c, marker='o')
pl.xlabel('x')
pl.ylabel('y')
pl.title('Plot of Two dimensional embeddings')
#pl.xlim(0.0, 10.)
pl.show()
