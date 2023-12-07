from string import punctuation
from os import listdir
import numpy
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
print("<>: Import lib sucessfull")
dataset = []
datasetDoc = []
datasetLable = []
with open("Tweets.csv", 'r', encoding='cp932', errors='ignore') as csvfile:
	# creating a csv reader object
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		if row[1] == "positive": 
			temp = [row[10], 1]
			dataset.append(temp)
			datasetDoc.append(row[10])
			datasetLable.append(1)
		elif row[1] == "negative":
			temp = [row[10], 0]
			dataset.append(temp)
			datasetDoc.append(row[10])
			datasetLable.append(0)
print(len(dataset))
print(dataset[0])
print("<>: Read data set have completed")
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
# turn a doc into clean tokens
def clean_doc(doc, vocab):
	# split into tokens by white space
	tokens = doc.split()
	# remove punctuation from each token
	table = str.maketrans('', '', punctuation)
	tokens = [w.translate(table) for w in tokens]
	# filter out tokens not in vocab
	tokens = [w for w in tokens if w in vocab]
	tokens = ' '.join(tokens)
	return tokens
 
# load all docs in a directory
# load all docs in a directory
def process_docs(doc, vocab, is_trian):
	documents = list()
	# walk through all files in the folder
	for data in doc:
		tokens = clean_doc(data, vocab)
		#add to list
		documents.append(tokens)
	return documents
 
# load embedding as a dict
def load_embedding(filename):
	# load embedding into memory, skip first line
	file = open(filename,'r')
	lines = file.readlines()[1:]
	file.close()
	# create a map of words to vectors
	embedding = dict()
	for line in lines:
		parts = line.split()
		# key is string word, value is numpy array for vector
		embedding[parts[0]] = asarray(parts[1:], dtype='float32')
	return embedding
 
# create a weight matrix for the Embedding layer from a loaded embedding
def get_weight_matrix(embedding, vocab):
	# total vocabulary size plus 0 for unknown words
	vocab_size = len(vocab) + 1
	# define weight matrix dimensions with all 0
	weight_matrix = zeros((vocab_size, 100))
	# step vocab, store vectors using the Tokenizer's integer mapping
	for word, i in vocab.items():
		weight_matrix[i] = embedding.get(word)
	return weight_matrix

# load the vocabulary
vocab_filename = 'vocab2.txt'
try:
	vocab = load_doc(vocab_filename)
	vocab = vocab.split()
	vocab = set(vocab)
	print("<>: Read file vocab successfull")
except:
	print("<Error>: Can not load file vocab2.txt Please stop this program at here. And check file vocab2.txt \n if it not exist, please run Addcocab2.py at first")
# load all training reviews
doctrain = datasetDoc[0:3999]
docTest = datasetDoc[4000:4199]
train_docs = process_docs(doctrain, vocab, True)
print(train_docs)
labletrain = datasetLable[0:3999]
lableTest = datasetLable[4000:4199]
labletrain = numpy.array(labletrain)
lableTest = numpy.array(lableTest)
print(labletrain)


# create the tokenizer
tokenizer = Tokenizer()
# fit the tokenizer on the documents
tokenizer.fit_on_texts(train_docs)
encoded_docs = tokenizer.texts_to_sequences(train_docs)
# pad sequences
max_length = max([len(s.split()) for s in train_docs])
Xtrain = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
# define training labels
ytrain = labletrain
#test===========
test_docs = process_docs(docTest, vocab, True)
# sequence encode
encoded_docs = tokenizer.texts_to_sequences(test_docs)
# pad sequences
Xtest = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
# define test labels
ytest = lableTest

# define vocabulary size (largest integer value)
vocab_size = len(tokenizer.word_index) + 1
print(max_length)
print(vocab_size)
# load all test reviews
model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=max_length))
model.add(Conv1D(filters=32, kernel_size=8, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print("<>: Biuld model successfull")
print(model.summary())
# compile network
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit network
print("<>: Start tranning model")
model.fit(Xtrain, ytrain, epochs=5, verbose=2)
# evaluate
loss, acc = model.evaluate(Xtest, ytest, verbose=0)
print("<>: Trainning model successfull")
print('<>: Model test:...Accuracy: %f and Loss: %f' % (acc*100, loss))
print("<>: ===================Model is ready to use=======================")
while True:
	print("==================================================================")
	myText = input("[]: Enter input text (maximum leng 100 word): ")
	print("<>: Your input text: " + myText)
	print("<>: Starting process your input text")
	tokens = clean_doc(myText, vocab)
	document = list()
	document.append(tokens)
	# fit the tokenizer on the documents
	encoded_docs = tokenizer.texts_to_sequences(document)
	print("<>: Processing input text is completed")
	print("<>: Your input text after processing")
	print(encoded_docs)
	# pad sequences
	inputModel = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
	print("<>: Starting predict with model")
	# define vocabulary size (largest integer value)
	yhat = model.predict(inputModel)
	print("<>: prediction is completed")
	print(yhat[0][0])
