import pickle
from lxml import html
import requests
import unicodedata

urls = open('data/urls.txt', 'r')

allStuff = []
num = 0

for x in urls:
	url = x
	print url
	print num
	page = requests.get(url)
	text = html.fromstring(page.text).find_class('entry-content')[0].text_content()
	date = html.fromstring(page.text).find_class('date published time')[0].text_content()
	obj = {}
	num = num + 1

	text_two = text.encode('utf-8','ignore')
	date_two = text.encode('utf-8','ignore')

	obj['content'] = text_two
	obj['date'] = date_two
	obj['url'] = url
	print url

	allStuff = allStuff + [obj]

pickle.dump( allStuff, open( "data/raw_scrape.p", "wb" ) )


