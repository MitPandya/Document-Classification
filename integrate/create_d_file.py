import re
import os
from os import listdir
from os.path import isfile, isdir, join,splitext,basename
import nltk
import numpy as np
from nltk import ne_chunk, word_tokenize
from multiprocessing import Pool
from itertools import chain
import string
from nltk.stem.lancaster import LancasterStemmer
from shutil import copyfile, copy, rmtree

#input_folder="./webkb_train/"
#input_folder="./r8_train/"
#input_folder="./r52_train/"
#input_folder="./cade_train/"
#input_folder = "../exp_bitbybit_bak_train/"
input_folder = "../20news-bydate"
stopwords = set(nltk.corpus.stopwords.words('english'))
out_file = 'documents.txt'
map_file = "doc_map.txt"
st = LancasterStemmer()

def process_file(file_path):
    file = open(file_path).read()
    # Remove punctuations from text
    text = re.sub('[^a-zA-Z \n\.]', '', file).strip()
    punkt = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = punkt.tokenize(text.lower())
    # since the tokenizer works on a per sentence level, we can parallelize
    p = Pool()
    words2 = list(chain.from_iterable(p.map(nltk.tokenize.word_tokenize, sentences)))
    p.close()
    # Now remove words that consist of only punctuation characters
    words2 = [word for word in words2 if not all(char in string.punctuation for char in word)]
    # Remove contractions - wods that begin with '
    words2 = [word for word in words2 if not (word.startswith("'") and len(word) <=2)]
    processed_text = filter(lambda word : word not in stopwords, words2)
    processed_text = map(lambda word: st.stem(word), processed_text)
    return ' '.join(processed_text)

print "processing files.."
c = 0
input_folders = [sub_dir for sub_dir in listdir(input_folder) if isdir(join(input_folder,sub_dir))]
output_file = open(out_file, 'w')
mapping_file = open(map_file, 'w')
output_file.write('7532')
try:
    file_id = 0
    train_files = {}
    test_files = {}
    all_files = {}
    root_dir_trainpath = input_folder + "-train/"
    root_dir_testpath = input_folder + "-test/"
    rmtree(root_dir_trainpath)
    rmtree(root_dir_testpath)

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
               train_files[file_path] = file_id
               file_id = file_id + 1
               copy(file_path, file_trainpath)
               label = file_path.split('/')[2]
               text = process_file(file_path)
               output_file.write('[ '+label+' ] '+text)
               output_file.write('\n')
               mapping_file.write('train-'+str(file_id)+file_path)
               mapping_file.write('\n')
               c += 1
          for file in test:
               file_path = dir_path + file
               file_testpath = dir_testpath + file
               test_files[file_path] = file_id
               file_id = file_id + 1
               copy(file_path, file_testpath)
               label = file_path.split('/')[2]
               text = process_file(file_path)
               output_file.write('[ '+label+' ] '+text)
               output_file.write('\n')
               mapping_file.write('test-'+str(file_id)+file_path)
               mapping_file.write('\n')
               c += 1

    print "splitting done"

finally:
    output_file.close()

print "done ",c