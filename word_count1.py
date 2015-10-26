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

def countInstances(toBeCounted):
	ret = {}
	for url in bag_of_words:
		if (str(bag_of_words[url]['month']) in ret):
			ret[bag_of_words[url]['month']] = ret[bag_of_words[url]['month']] + sum(map(lambda x: toBeCounted.count(x), bag_of_words[url]['words']))
		else:
			ret[bag_of_words[url]['month']] = sum(map(lambda x: toBeCounted.count(x), bag_of_words[url]['words']))
	return ret

to_examine = {}
#knowledg, known, invalid, insight, 'assum','assumpt',
to_examine['gay_concerns'] = ['lgbt','gay','lesbian','queer','homosexu']
to_examine['reason_concerns'] = ['argu','curios','curious','doubt','experimenti','experiment','experienc','fallaci','heurist','invalid','logic','predict','premis','prove','proven','ration','evid','agreement','rebutt','rebut']
to_examine['community_concerns'] = ['communiti','communion']
to_examine['transhumanist_concerns'] = ['transhuman','transhumanist']
to_examine['math_concerns'] = ['topolog','math','mathemat']



for name in to_examine:
	instances = countInstances(to_examine[name])
	f = open('data/' + name  + '.csv', 'w')
	for n in sorted(instances.keys()):
		f.write(str(n) + ", " + str(instances[n]) + '\n')
	f.close

print "done!"











