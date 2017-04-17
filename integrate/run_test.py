import numpy as np
from sklearn.svm import SVC
from sklearn import metrics

train_files = {}
test_files = {}
doc_label = {}

results_svc=open("../results_svc.txt" ,"w")

doc_map = open('doc_map.txt', 'r')

for lines in doc_map:
  l = lines.strip()
  id = int(l.split('..')[0].split('-')[1])
  label = l.split('..')[1].split('/')[2]
  type = l.split('..')[0].split('-')[0]
  doc_label[id] = label

  if type == 'train':
    train_files[id] = label
  elif type == 'test':
    test_files[id] = label

j = 0
train_data = []
test_data = []
train_label = []
test_label = []
print "====================================================="
data = np.loadtxt('../edges.embeddings')
print data
for i in data[:,0]:
  z=[]
  for k in data[j,1:len(data[j])]:
    z.append(k)
  if i in train_files.keys():
    train_data.append(z)
    #train_label.append(label_ids[doc_label[i]])
    train_label.append(doc_label[i])
  else:
    if i in test_files.keys():
      test_data.append(z)
      #test_label.append(label_ids[doc_label[i]])
      test_label.append(doc_label[i])
  j = j + 1
       
#Classify - it and write metrics
'''knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(train_data,train_label)
y1=knn.predict(test_data)
#print "Predicted:", y1
#print "Actual:", test_label
print("KNN: ", metrics.precision_recall_fscore_support(test_label, y1, average='micro'))
print("KNN: ", metrics.precision_recall_fscore_support(test_label, y1))
results_knn.write("\nIteration: " + str(iter) + "\n")
results_knn.write(metrics.classification_report(test_label, y1))'''
  
svc = SVC(C=20.0) # experiment with C-values
svc.fit(train_data,train_label)
y1=svc.predict(test_data)
print("SVC: ", metrics.precision_recall_fscore_support(test_label, y1, average='micro'))
results_svc.write("\nIteration: " + str(iter) + "\n")
results_svc.write(metrics.classification_report(test_label, y1))
 
#results_knn.close() 
results_svc.close()