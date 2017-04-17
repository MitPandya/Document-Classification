import sys
from collections import Counter

phi_file = open('model-final.phi', 'r')
a = []
b = []
topic_dict = {}

# try

# 0.0075
# 0.01
# 0.02
# 0.03
# Labeled LDA
# 1. plain labeled lda -> each document 1 label
# 2. semi-labeled lda -> each document 1 label and N common labels ( threshold : )
# 

threshold = 0.02

for line in phi_file:
	a.append(line)

for i in range(len(a)):
	b.append(a[i].split(' '))

for i in range(len(b)):
	b[i] = b[i][:-1]
	b[i] = map(lambda x: float(eval(x)), b[i])
	temp = []
	for j in range(len(b[i])):
		if b[i][j] >= threshold:
			temp.append(j)
	topic_dict[i] = temp
phi_file.close()

'''f = []
file1 = open('model-final.theta', 'r')
for lines in file1:
	f.append(lines)

g = []
for i in range(len(f)):
	g.append(f[i].split(' '))

for i in range(len(g)):
	g[i] = g[i][:-1]
	g[i] = map(lambda x: float(eval(x)), g[i])'''


# Reading documents from documents.txt file
doc_file = open('documents.txt', 'r')
docs = []
for lines in doc_file:
	docs.append(lines)
docs = docs[1:]
doc_file.close()

# to extract data from wordmap.txt
wordmap_file = open('wordmap.txt', 'r')
word_map = {}
i = 0
for lines in wordmap_file:
	if i > 0:
		temp = lines.replace('\n', '').split(' ')
		word_map[temp[0]] = int(temp[1])
	i = 1
wordmap_file.close()

file = open('edges.txt','w')

'''print "writing to edges.txt file..."
for l in range(len(docs)):
	for i in range(len(topic_dict)):
		for j in range(len(topic_dict[i])):
			temp = topic_dict[i][j]
			if temp in word_map:
				word = word_map[temp]
				if word in docs[l]:
					#file.write(%(l, temp + len(docs)))
					file.write('%d %s' % (l,word))
					file.write('\n')
print "done!"'''
print "writing to edges.txt file..."
w = 0
x = 0
for l in range(len(docs)):
	doc_words = docs[l].split(' ')
	for k in range(len(doc_words)):
		cur_word = doc_words[k].strip()
		word_id = word_map[cur_word]
		for j in range(len(topic_dict)):
			if word_id in topic_dict[j]:
				file.write('%d %d' % (l, word_id + 10000 + j + len(docs)))
				file.write('\n')
				w += 1
		file.write('%d %d' % (l, word_id + 10000 ))
		file.write('\n')
		x += 1
print "done!"
print 'w,x',w,x
