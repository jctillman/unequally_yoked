import cPickle
import csv
import math
from stemming.porter2 import stem

def strip(text, toBeStripped):
	for char in toBeStripped:
		text = text.replace(char,'')
	return text

def only(text, only):
	m = 0
	for char in text:
		if char not in only:
			text = text[:m] + ' ' + text[m+1:] 
		m = m + 1
	return text

data = cPickle.load( open( "data/raw_scrape.p", "rb" ))
bag_of_words = {}
all_words_whatsoever = []
for n in range(len(data)):
	dtm = data[n]
	url = dtm['url']
	if 'christian-entry' not in url and 'atheist-entry' not in url and 'christian-answer' not in url and 'atheist-answer' not in url and 'atheism-answer' not in url:
		text = dtm['content']
		reduced = only(text, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
		lower = reduced.lower()
		split = lower.split(' ')
		words = filter(lambda x: len(x) > 2, split)
		stemmed = map(stem, words)
		key = dtm['url'][44:51]
		bag_of_words[url] = {'month': key, 'words': stemmed}
		all_words_whatsoever = all_words_whatsoever + stemmed


print bag_of_words

setted = list(set(all_words_whatsoever))

word_frequency = {}
for word in setted:
	times = 0
	for url in bag_of_words:
		if bag_of_words[url]['words'].count(word) > 0:
			times = times + 1
	print word
	word_frequency[word] = times

#print word_frequency

filtered_word_frequency = {}
num_articles = len(bag_of_words.keys())
lower = num_articles * 0.0075;
higher = num_articles * 0.3;
print "lower " + str(lower)
print "higher " + str(higher)
for word in word_frequency:
	if word_frequency[word] > lower and word_frequency[word] < higher:
		filtered_word_frequency[word] = word_frequency[word]


#output of the above code-- words which seem reasonably 
#specific and also reasonably common

all_words = sorted(filtered_word_frequency.keys())


notArr = {};
for url in bag_of_words:
	notArr[url] = []
	for word in all_words:
		temp = 100 * float(bag_of_words[url]['words'].count(word)) / float(len(bag_of_words[url]['words']))
		notArr[url] = notArr[url] + [temp]


cPickle.dump({'data': notArr, 'urls': bag_of_words.keys(), 'words': all_words}, open("data/bag_of_words.p", "wb"))
