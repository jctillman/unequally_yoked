import cPickle
from sklearn import cluster
import numpy as np

spectral = cluster.KMeans(n_clusters=30, max_iter=500, n_init=2000)
#spectral = cluster.AgglomerativeClustering()
print "Loading..."
tfidf = cPickle.load( open( "data/bag_of_words.p", "rb" ) )
print "Loaded..."
nped = tfidf['data']
words = tfidf['words']

gotten = []
for arr in nped:
	gotten = gotten + [nped[arr]]

got = np.array(gotten)


print "Fitting..."
spectral.fit(got)
print "Fitted..."


print len(spectral.cluster_centers_);

clusters = {}

f = open( "data/keywords.csv", "w")
num = 0
for centroid in spectral.cluster_centers_:
	matched = zip(centroid, words)
	f.write(str(num) + '\n')
	sortd = sorted(matched, key = lambda x: -x[0])
	print sortd[0:30]
	for n in sortd[0:30]:
		f.write(n[1] + ", " + str(n[0]) + '\n')
	f.write( ' endline \n\n\n\n\n')
	num = num + 1
f.close()


finished = {}


for idc, n in enumerate(nped):
	finished[n] = spectral.labels_.astype(np.int)[idc]

cPickle.dump(finished, open("data/clusters.p", "wb"))