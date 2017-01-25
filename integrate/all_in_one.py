import re
import os
import numpy as np
import shutil
import codecs
from os import listdir
from os.path import isfile, isdir, join,splitext,basename
from shutil import copyfile, copy, rmtree
from subprocess import call
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

#input_folder="./exp_bitbybit_bak"
#input_folder="./20news-bydate"
input_folder="./webkb"
#input_folder="./r8"
#input_folder="./r52"
#input_folder="./cade"

results_knn=open("./results_knn.txt" ,"w")
results_svc=open("./results_svc.txt" ,"w")

for iter in range(1,11):
  #First split the data
  input_folders = [sub_dir for sub_dir in listdir(input_folder) if isdir(join(input_folder + "/", sub_dir))]
  root_dir_trainpath = input_folder + "_train/"
  root_dir_testpath = input_folder + "_test/"
  rmtree(root_dir_trainpath)
  rmtree(root_dir_testpath)

  file_id = 0;
  
  #map of filenames to ids
  train_files = {}
  test_files = {}
  all_files = {}

  for folder in input_folders:
      dir_path = input_folder + str("/") +  folder + str("/")
      dir_trainpath = root_dir_trainpath  + folder + str("/")
      dir_testpath = root_dir_testpath + folder + str("/")
      #print "Splitting: " , dir_path
      files = [ f for f in listdir(dir_path) if isfile(join(dir_path,f))]
      #training = [ f for f in listdir(dir_trainpath) if isfile(join(dir_trainpath,f))]
      #test = [ f for f in listdir(dir_testpath) if isfile(join(dir_testpath,f))]
      np.random.shuffle(files)
      train_idx = int(0.7 * len(files))
      training, test = files[:train_idx], files[train_idx:]
      os.makedirs(dir_trainpath)
      os.makedirs(dir_testpath)
      for file in training:
           file_path = dir_path + file
           file_trainpath = dir_trainpath + file
           train_files[file_path] = file_id;
           file_id = file_id + 1; 
           copy(file_path, file_trainpath)
      for file in test:
           file_path = dir_path + file
           file_testpath = dir_testpath + file
           test_files[file_path] = file_id;
           file_id = file_id + 1; 
           copy(file_path, file_testpath)
  print "splitting done"
  #print test_files
  all_files=train_files.copy()
  all_files.update(test_files)

  #Now create the controlset  
  call(["python", "top_keys.py"])

  #Now create the graph
  indicator_id = 50000;
  noun_id = 60000;
  doc = ""
  
  #more maps
  doc_label={}
  label_ids={}
  nouns={}
  edges=open("./edges.txt" ,"w")
  
  #now for the control set
  #load the control set first
  controlset_folder = "./controlset/"
  controlset_words ={}
  start_ids ={}
  for file in listdir(controlset_folder): 
    print "Loading controlset ...", file
    words=codecs.open(controlset_folder + file, encoding="utf-8", errors='ignore')
    #words = open(controlset_folder + file).read()
    label=file.split("_keys")[0]
    for line in words:
      controlset_words[label]=line.split()
      start_ids[label]=indicator_id
      indicator_id = indicator_id + len(line.split())
  
  #go through the files and draw the edges
  for file in all_files.keys():
    no_edgeto_indicators = True
    file_with_noindicators = 0
    #print "Processing ", file, " ..."
    doc=codecs.open(file, encoding="utf-8", errors='ignore')
    #doc=open(file).read()
    for line in doc:
      line = line.replace("[.,;?!()<>{}*\\-'\"|:@%^&0-9]", " ")
      words = line.split()
      for word in words:
        #first try the control words
        curr_position = 50000
        prev_position = 50000
        curr_label = "" 
        for label in controlset_words.keys():
           curr_words = controlset_words[label]
           if word in curr_words:
             if curr_words.index(word) < curr_position:
               #print "Found a good posistion"
               prev_position = curr_position
               curr_position = curr_words.index(word)
               curr_label = label
               #print "Current label", curr_label
        if curr_label != "":
          #print "Found indicator..."
          edges.write(str(all_files[file]) + "\t" +  str(start_ids[curr_label]+curr_position) + "\n") 
          no_edgeto_indicators = False
        else:  
          try:
            exists = nouns[word]
          except KeyError:
            noun_id = noun_id + 1
            nouns[word]=noun_id
          edges.write(str(all_files[file]) + "\t" +  str(nouns[word]) + "\n") 
    label = file.split("/")[2]
    doc_label[all_files[file]]=label
    #print label
    #if it is a training file draw another edge
    try:
      exists = label_ids[label] 
    except KeyError:
      indicator_id = indicator_id + 1
      label_ids[label] = indicator_id
    #for training file draw this edge as well
    if file in train_files.keys():
      edges.write(str(all_files[file]) + "\t" +  str(label_ids[label]) + "\n") 
    if no_edgeto_indicators == True:
      print "No edge to indicators for file:", file
      file_with_noindicators = file_with_noindicators + 1
      print "File with no indicators: ", file_with_noindicators
    
  #close the file     
  edges.close()
  
  #print train_files
  #print test_files
  #print label_ids  
  #print doc
  #print controlset_words
  
  #Run deepwalk
  #deepwalk --format edgelist --input /home/vijoy/deepwalk/edges.txt --output /home/vijoy/deepwalk/edges.embeddings --representation-size 2
  cmd = "deepwalk --format edgelist --input ./edges.txt --output ./edges.embeddings --representation-size 128"
  call(cmd.split())
  #remove the first line
  cmd1 = "sed -i 1d edges.embeddings" 
  call(cmd1.split())
  
  #Get only the doc embeddings
  j = 0
  train_data = []
  test_data = []
  train_label = []
  test_label = []
  data = np.loadtxt('edges.embeddings')
  for i in data[:,0]:
    z=[]
    for k in data[j,1:len(data[j])]:
      z.append(k)
    if i in train_files.values():
      train_data.append(z)
      #train_label.append(label_ids[doc_label[i]])
      train_label.append(doc_label[i])
    else:
      if i in test_files.values():
        test_data.append(z)
        #test_label.append(label_ids[doc_label[i]])
        test_label.append(doc_label[i])
    j = j + 1
       
  #Classify - it and write metrics
  knn = KNeighborsClassifier(n_neighbors=3)
  knn.fit(train_data,train_label)
  y1=knn.predict(test_data)
  #print "Predicted:", y1
  #print "Actual:", test_label
  print("KNN: ", metrics.precision_recall_fscore_support(test_label, y1, average='micro'))
  print("KNN: ", metrics.precision_recall_fscore_support(test_label, y1))
  results_knn.write("\nIteration: " + str(iter) + "\n")
  results_knn.write(metrics.classification_report(test_label, y1))
  
  svc = SVC(C=20.0)
  svc.fit(train_data,train_label)
  y1=svc.predict(test_data)
  print("SVC: ", metrics.precision_recall_fscore_support(test_label, y1, average='micro'))
  results_svc.write("\nIteration: " + str(iter) + "\n")
  results_svc.write(metrics.classification_report(test_label, y1))
 
results_knn.close() 
results_svc.close() 
