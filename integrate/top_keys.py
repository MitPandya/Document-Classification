import re
import os
import numpy as np
import shutil
from os import listdir
from os.path import isfile, isdir, join,splitext,basename
from shutil import copyfile, copy
from subprocess import call

input_folder="./webkb_train/"
#input_folder="./r8_train/"
#input_folder="./r52_train/"
#input_folder="./cade_train/"
input_folders = [sub_dir for sub_dir in listdir(input_folder) if isdir(join(input_folder,sub_dir))]
for folder in input_folders:
    dir_path = input_folder + folder + str("/")
    print "Generating mallet file ... " , dir_path
    #bin/mallet import-dir --input ~/deepwalk/exp_bitbybit_train_bak/arts_creative_writing --output arts_creative_writing.mallet --keep-sequence
    call(["/home/vijoy/mallet/mallet-2.0.7/bin/mallet", "import-dir", "--input", dir_path, "--output", "test.mallet", "--keep-sequence" ])
    print "Generating topkeywords file ... " , dir_path
    #if not os.path.exists("./" + folder):
    #  os.makedirs("./" + folder)
    output_path = "./controlset/" + folder + "_keys.txt"
    #bin/mallet train-topics --input topic-input.mallet --num-topics 1 --output-topic-keys test_keys.txt --num-top-words 100
    call(["/home/vijoy/mallet/mallet-2.0.7/bin/mallet", "train-topics", "--input", "test.mallet", "--num-topics", "1", "--output-topic-keys", output_path, "--num-top-words", "100" ])
print "done"
