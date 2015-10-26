import cPickle

id = cPickle.load( open( "data/clusters.p", "rb" ) )

record = {}
for m in sorted(id.keys()):
	month = m[44:51]
	if month not in record:
		record[month] = {}
	if id[m] not in record[month]:
		record[month][id[m]] = 1
	else:
		record[month][id[m]] = record[month][id[m]] + 1
	if id[m] == 0:
		print m

for n in range(30):
	f = open( "data/urls_for_cluster_" + str(n) + ".csv", "w")
	for m in sorted(id.keys()):
		if str(id[m]) == str(n):
			print m
			f.write(m)
	f.close()

print "Clustering counts:"
counts = {}
f = open('data/clustered.csv', 'w')
for m in sorted(record.keys()):
	string = m 
	for num in range(30):
		if num in record[m]:
			string = string + ", " + str(record[m][num])
		else:
			string = string + ", 0"
	f.write(string + '\n')

