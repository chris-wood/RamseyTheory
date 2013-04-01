f = open("graph81.mat", "r")
f2 = open("graph81.mat.mod", "w")
f2.write(" ")
for line in f:
	length = len(line)
	for i in range(length):
		f2.write(line[i] + " ")
	f2.write("")