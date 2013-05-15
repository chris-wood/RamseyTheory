import sys
from numpy import *

f = open(sys.argv[1], 'r')
na = int(sys.argv[2])
times = []
for l in f:
	l = l.replace("\n","")
	if (l.startswith("(") and l.endswith(")")):
		splits = l.split(",")
		time = splits[len(splits) - 1].strip()
		value = time[0:len(time) - 1].strip()
		times.append(float(value))
avg = average(times)
print(float((2**na)) * avg)