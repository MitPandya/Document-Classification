import numpy as np
import pylab as pl
from sklearn.cluster import KMeans, SpectralClustering
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 

# Use numpy to load the data contained in the file
#data = np.loadtxt('onlydoc_with3indicators.embeddings')
data = np.loadtxt('onlydoc_all_128.embeddings')
#data = np.loadtxt('onlydoc_all_10.embeddings')
# plot the first column as x, and second column as y
c=[]
x=[]
y=[]
j=0

d = {}
counts = {}
with open("file_class.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[int(key)] = int(val)
       try:
         counts[int(val)] = counts[int(val)] + 1
       except KeyError:
         counts[int(val)] = 1

#print counts

for i in data[:,0]:
  #x.append([data[j,1],data[j,2]])
  #x.append([data[j,1], data[j,2], data[j,3], data[j,4], data[j,5], data[j,6], data[j,7], data[j,8], data[j,9], data[j,10]])
  z=[]
  for k in data[j,1:len(data[j])]:
    z.append(k)
  x.append(z)
  y.append(d[i])
  j=j+1
  #if i < 33:
  #  c.append('red')
  #  y.append(0)
  #else:
  #  if i < 66:
  #    c.append('blue')
  #    y.append(1)
  #  else:
  #   c.append('green')
  #   y.append(2)
#print x
print len(y)
print len(x)
#print y

gnb = GaussianNB()
gnb.fit(x[1:4447],y[1:4447])
y1=gnb.predict(x[4448:4941])
print("Gaussian: ", metrics.precision_recall_fscore_support(y[4448:4941], y1, average='micro'))
#print("Predicted:", y1)

knn = KNeighborsClassifier(n_neighbors=3) 
#knn.fit(x[1:118],y[1:118])
knn.fit(x[1:4447],y[1:4447])
#y1=knn.predict(x[119:130])
y1=knn.predict(x[4448:4941])
#print("Predicted:", y1)
#print(y[119:130])
#print("Actual", y[4448:4941])
#print(metrics.precision_recall_fscore_support(y[119:130], y1))
print(metrics.precision_recall_fscore_support(y[4448:4941], y1, average='micro'))

#print(knn.predict([[0.005112,-0.046462,-0.159422,-0.099351,0.227360,-0.042506,0.115936,0.126921,-0.126383,0.148245,0.319643,-0.031282,0.056544,-0.000627,0.015725,-0.085918,-0.030907,-0.249490,0.027212,-0.137115,0.181182,-0.150460,0.010726,-0.144732,-0.116934,-0.116293,-0.147572,-0.018462,0.164010,0.150961,-0.044382,-0.217379,0.133727,0.141625,-0.104455,0.024281,-0.009089,0.126656,-0.092566,0.031840,0.164499,-0.159959,-0.090911,0.028096,-0.140781,0.023171,0.101124,-0.035135,0.099629,-0.091998,-0.071872,0.052892,0.171598,-0.000570,-0.104986,-0.061017,0.058763,-0.030384,0.135418,-0.202513,-0.214985,0.183316,0.222563,-0.165795,-0.272334,0.027117,-0.152521,0.160412,0.021701,-0.045508,0.024952,0.189379,-0.020058,-0.185879,0.029140,-0.006944,0.190678,0.092100,0.126240,0.125272,-0.034706,0.063062,-0.028506,-0.187083,-0.018370,-0.066662,0.223519,0.127452,-0.122273,0.028319,0.170374,0.025925,-0.010086,-0.172795,-0.000026,0.096173,0.066806,0.103348,-0.096974,-0.196987,0.075588,0.005152,-0.255471,-0.049246,-0.191401,-0.020285,0.004324,-0.078057,-0.141483,0.097589,-0.269434,-0.065810,-0.036227,0.017676,-0.059508,0.191977,0.047431,-0.069312,0.030059,0.022119,0.120999,0.152056,-0.030785,0.204020,-0.033653,-0.109620,0.034062,-0.061724]]))

#print(knn.predict([[-0.341543, -0.224698, 0.159681, 0.735977, -0.070716, -0.300738, -0.318239]]))
#print(knn.predict([[-0.518611, -0.838737, -0.288385, 0.503242, -0.400460, 0.177740, 0.280273]]))
#print(knn.predict([[-0.258175, -0.148608, -1.199669, -0.952295, -0.103700, 0.474609, 0.736614]]))
#kmeans = KMeans(n_clusters=49, random_state=2)
#kmeans.fit(x)
#print("Clustered", specClustering.labels_)
#print("Actual", y)
print(metrics.precision_recall_fscore_support(y, kmeans.labels_, average='micro'))
#print(metrics.precision_recall_fscore_support(y, specClustering.labels_))
#print("Adjusted random score", metrics.adjusted_rand_score(y, kmeans.labels_))
#print(metrics.homogeneity_score(y, kmeans.labels_))
#print(metrics.completeness_score(y, kmeans.labels_))

#pl.scatter(data[:,1], data[:,2], s=50, c=c, marker='o')
#pl.xlabel('x')
#pl.ylabel('y')
#pl.title('Plot of Two dimensional embeddings')
#pl.show()
