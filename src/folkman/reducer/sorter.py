import sys
f = open(sys.argv[1],'r')

sortedFiles = []

for fileName in f:
	f2 = open(fileName.strip(), 'r')
	l1 = f2.readline().strip().strip("\n")
	l2 = f2.readline().strip().strip("\n")
	l1d = l1.split(" ")
	l2d = l2.split(" ")
	n2 = float(l1d[1])
	n3 = float(l2d[3])
	ratio = n2/n3

	index = 0
	fin = False
	for p in sortedFiles:
		if ratio > p[0]:
			sortedFiles.insert(index, (ratio, fileName.strip()))
			fin = True
			break
		index = index + 1
	if fin == False:
		sortedFiles.insert(len(sortedFiles), (ratio, fileName.strip()))

# print sorted output
for p in sortedFiles:
	print(p[1])
