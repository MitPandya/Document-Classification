###########
#NEW NEW NEW
###########
A new folder called integrate has been added. 
all_in_one.py 
=============
- takes the data
- splits it into train and test 
- Runs LDA on train to generate the controlset
- Genrates the graph
- Runs deepwalk and
- Predicts labels for test data and prints out classification report
- It can do this for multiple splits in a loop

Requirements:
- deepwalk
- mallet (specify path in code; top_keys.py)









# deepwalk-classify
This repository uses deepwalk to classify text documents. To run:
- Create the nouns only from the original documents (java code in src folder) - You will need the standford pos tagger as a dependency.
- Create the graph as an edge list. (java code in src folder)
- pip or conda install the deepwalk library https://github.com/phanein/deepwalk
- Run this:
deepwalk --format edgelist --input ./edges.txt --output ./edges.embeddings --representation-size 2
- To get only the document ids from the embeddings run the getOnlyDocs() method in edu.ncsu.deepwalk.CreateEdgeList class
- To plot the resultant files run python plotIt.py
- You may need to install some python dependencies
