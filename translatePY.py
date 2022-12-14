# -*- coding: utf-8 -*-
import string
import re
import pandas as pd
import numpy as np

from pickle import load, dump
from unicodedata import normalize
from numpy import array, argmax
from numpy.random import rand, shuffle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu




# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, mode='rt', encoding='utf-8')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text
# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))
 
# save a list of clean sentences to file
def save_clean_data(sentences, filename):
	dump(sentences, open(filename, 'wb'))
	print('Saved: %s' % filename)

from google.colab import drive
drive.mount("/content/drive")

# load dataset
filename = "/content/drive/My Drive/Latin Translation ML project/Dataset1.csv"
doc = load_doc(filename)

dataset_original = pd.read_csv(filename,converters={i: str for i in range(0, 2)})
dataset_original

clean_pairs= dataset_original.to_numpy()

# save clean pairs to file
save_clean_data(clean_pairs, 'english-latin.pkl')
# spot check
for i in range(100):
	print('[%s] => [%s]' % (clean_pairs[i,0], clean_pairs[i,1]))
 
# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))
 
# save a list of clean sentences to file
def save_clean_data(sentences, filename):
	dump(sentences, open(filename, 'wb'))
	print('Saved: %s' % filename)

# load dataset
raw_dataset = load_clean_sentences('english-latin.pkl')
# random shuffle
shuffle(raw_dataset)
# reduce dataset size
n_sentences = 13000
dataset = raw_dataset[:n_sentences]
# split into train/test
train, test = dataset[:11000], dataset[11000:]
# save
save_clean_data(dataset, 'english-latin-both.pkl')
save_clean_data(train, 'english-latin-train.pkl')
save_clean_data(test, 'english-latin-test.pkl')


# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))
 
# fit a tokenizer
def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer
 
# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)
 
# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X
 
# one hot encode target sequence
def encode_output(sequences, vocab_size):
	ylist = list()
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size)
		ylist.append(encoded)
	y = array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y
 
# define NMT model
def define_model(src_vocab, tar_vocab, src_timesteps, tar_timesteps, n_units):
	model = Sequential()
	model.add(Embedding(src_vocab, n_units, input_length=src_timesteps, mask_zero=True))
	model.add(LSTM(n_units))
	model.add(RepeatVector(tar_timesteps))
	model.add(LSTM(n_units, return_sequences=True))
	model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
	return model
 
# load datasets
dataset = load_clean_sentences('english-latin-both.pkl')
train = load_clean_sentences('english-latin-train.pkl')
test = load_clean_sentences('english-latin-test.pkl')
 
# prepare english tokenizer
eng_tokenizer = create_tokenizer(dataset[:, 0])
eng_vocab_size = len(eng_tokenizer.word_index) + 1
eng_length = max_length(dataset[:, 0])

# prepare latin tokenizer
lat_tokenizer = create_tokenizer(dataset[:, 1])
lat_vocab_size = len(lat_tokenizer.word_index) + 1
lat_length = max_length(dataset[:, 1])

# prepare training data
trainX = encode_sequences(lat_tokenizer, lat_length, train[:, 1])
trainY = encode_sequences(eng_tokenizer, eng_length, train[:, 0])
trainY = encode_output(trainY, eng_vocab_size)
# prepare validation data
testX = encode_sequences(lat_tokenizer, lat_length, test[:, 1])
testY = encode_sequences(eng_tokenizer, eng_length, test[:, 0])
testY = encode_output(testY, eng_vocab_size)

# define model
model = define_model(lat_vocab_size, eng_vocab_size, lat_length, eng_length, 256)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
# summarize defined model
print(model.summary())
plot_model(model, to_file='Latinmodel2.png', show_shapes=True)
# fit model
filename = 'Latinmodel2.h5'
checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
model.fit(trainX, trainY, epochs=120, batch_size=64, validation_data=(testX, testY), callbacks=[checkpoint], verbose=2)

tk = Tokenizer()

model_path = '/content/Latinmodel2.h5'

model = load_model(model_path)

def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)
# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
 
# evaluate the skill of the model
def evaluate_model(model, tokenizer, sources, raw_dataset):
	actual, predicted = list(), list()
	for i, source in enumerate(sources):
		# translate encoded source text
		source = source.reshape((1, source.shape[0]))
		translation = predict_sequence(model, eng_tokenizer, source)
		raw_target, raw_src = raw_dataset[i]
		if i < 10:
			print('src=[%s], target=[%s], predicted=[%s]' % (raw_src, raw_target, translation))
		actual.append([raw_target.split()])
		predicted.append(translation.split())
	# calculate BLEU score
	print('BLEU-1: %f' % corpus_bleu(actual, predicted, weights=(1.0, 0, 0, 0)))
	print('BLEU-2: %f' % corpus_bleu(actual, predicted, weights=(0.5, 0.5, 0, 0)))
	print('BLEU-3: %f' % corpus_bleu(actual, predicted, weights=(0.3, 0.3, 0.3, 0)))
	print('BLEU-4: %f' % corpus_bleu(actual, predicted, weights=(0.25, 0.25, 0.25, 0.25)))
 
# load datasets
dataset = load_clean_sentences('english-latin-both.pkl')
train = load_clean_sentences('english-latin-train.pkl')
test = load_clean_sentences('english-latin-test.pkl')
# prepare english tokenizer
eng_tokenizer = create_tokenizer(dataset[:, 0])
eng_vocab_size = len(eng_tokenizer.word_index) + 1
eng_length = max_length(dataset[:, 0])
# prepare latin tokenizer
lat_tokenizer = create_tokenizer(dataset[:, 1])
lat_vocab_size = len(lat_tokenizer.word_index) + 1
lat_length = max_length(dataset[:, 1])
# prepare data
trainX = encode_sequences(lat_tokenizer, lat_length, train[:, 1])
testX = encode_sequences(lat_tokenizer, lat_length, test[:, 1])
 
# load model
model = load_model('Latinmodel2.h5')
# test on some training sequences
print('train')
evaluate_model(model, lat_tokenizer, trainX, train)
# test on some test sequences
print('test')
evaluate_model(model, lat_tokenizer, testX, test)