
from string import punctuation
from os import listdir
from numpy import array
from numpy import asarray
from numpy import zeros
from collections import Counter
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
import csv
print("import sucess")
# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# turn a doc into clean tokens
def clean_doc(doc):
	# split into tokens by white space
	tokens = doc.split()
	# remove punctuation from each token
	table = str.maketrans('', '', punctuation)
	tokens = [w.translate(table) for w in tokens]
	# remove remaining tokens that are not alphabetic
	tokens = [word for word in tokens if word.isalpha()]
	# filter out stop words
	stop_words = set(stopwords.words('english'))
	tokens = [w for w in tokens if not w in stop_words]
	# filter out short tokens
	tokens = [word for word in tokens if len(word) > 1]
	return tokens
 
# load all docs in a directory
# load all docs in a directory
def process_docs(dataset, vocab, is_trian):
	# walk through all files in the folder
	for data in dataset:
		add_doc_to_vocab(data[0], vocab)
 
# load doc and add to vocab
def add_doc_to_vocab(text, vocab):
	# clean doc
	tokens = clean_doc(text)
	# update counts
	vocab.update(tokens)

dataset = []
with open("Tweets.csv", 'r', encoding='cp932', errors='ignore') as csvfile:
	# creating a csv reader object
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		if row[1] == "positive": 
			temp = [row[10], 1]
			dataset.append(temp)
		elif row[1] == "negative":
			temp = [row[10], 0]
			dataset.append(temp)
print(len(dataset))
print(dataset[0])

vocab = Counter()
# add all docs to vocab
process_docs(dataset, vocab, True)
# print the size of the vocab
print(len(vocab))
min_occurane = 2
tokens = [k for k,c in vocab.items() if c >= min_occurane]
print(tokens)

# save list to file
def save_list(lines, filename):
	# convert lines to a single blob of text
	data = '\n'.join(lines)
	# open file
	file = open(filename, 'w')
	# write text
	file.write(data)
	# close file
	file.close()
 
# save tokens to a vocabulary file
save_list(tokens, 'vocab2.txt')