
from lxml import html
import requests

pages = [];
for x in range(1,231):
	pages = pages + ['http://www.patheos.com/blogs/unequallyyoked/posts/page/' + str(x)]

url = []
for base_page in pages:
	page = requests.get(base_page)
	tree = html.fromstring(page.text)
	#buyers = tree.find_class('.entry_title')
	links = tree.iterlinks()
	links = filter(lambda x: x[2].find('patheos.com/blogs/unequally') != -1, links)
	links = filter(lambda x: x[2].find('#') == -1, links)
	links = filter(lambda x: x[2].find('author') == -1, links)
	links = filter(lambda x: x[2].find('tag') == -1, links)
	links = filter(lambda x: x[2].find('category') == -1, links)
	links = filter(lambda x: x[2].find('files') == -1, links)
	links = filter(lambda x: x[2].find('posts') == -1, links)
	links = filter(lambda x: ( x[2].find('2010') != -1 or x[2].find('2011') != -1 or x[2].find('2012') != -1 or x[2].find('2013') != -1 or x[2].find('2014') != -1 or x[2].find('2015') != -1 ), links)
	for link in links:
		if link[2] not in url:
			url = url + [link[2]]

f = open('data/urls.txt', 'w')
for m in url:
	f.write(m)
	f.write('\n')

f.close()

print tree
