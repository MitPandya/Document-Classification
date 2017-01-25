import re
import os
import numpy as np
import shutil
from os import listdir
from os.path import isfile, isdir, join,splitext,basename
from shutil import copyfile, copy

input_folder="./exp_bitbybit_bak/"
input_folders = [sub_dir for sub_dir in listdir(input_folder) if isdir(join(input_folder,sub_dir))]
root_dir_trainpath = input_folder.replace("bitbybit", "bitbybit_train")
root_dir_testpath = input_folder.replace("bitbybit", "bitbybit_test")
for folder in input_folders:
    dir_path = input_folder + folder + str("/")
    dir_trainpath = root_dir_trainpath  + folder + str("/")
    dir_testpath = root_dir_testpath + folder + str("/")
    print "Splitting: " , dir_path
    files = [ f for f in listdir(dir_path) if isfile(join(dir_path,f))]
    np.random.shuffle(files)
    train_idx = int(0.9 * len(files))
    training, test = files[:train_idx], files[train_idx:]
    os.makedirs(dir_trainpath)
    os.makedirs(dir_testpath)
    for file in training:
         file_path = dir_path + file
         file_trainpath = dir_trainpath + file
         copy(file_path, file_trainpath)
    for file in test:
         file_path = dir_path + file
         file_testpath = dir_testpath + file
         copy(file_path, file_testpath)
print "done"
#return (root_dir_trainpath, root_dir_testpath)
