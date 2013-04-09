f = open('out','r')
for line in f:
	if (line.startswith("CPU time")):
		data = line.split(" ")
		time = float(data[len(data) - 2]) # CPU _ Time _ : _ <time here>
		print(time)
