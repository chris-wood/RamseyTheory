#!/usr/bin/python

#
# File: experiment.py
# Author: Christopher A. Wood, caw4567@rit.edu
# Description: Run the SAT experiments and extract the times...
#

import sys
import subprocess
import os
import shutil
import signal
from time import sleep

if (len(sys.argv) != 2):
	print "Usage: python experiment.py fileList"
else:
	inputFile = sys.argv[1]
	files = open(inputFile, 'r')
	times = []

	sleepInterval = 5
	cutoff = 1800

	for f in files:
		f = f.strip()
		print >> sys.stderr, "Running: " + str(f)
		elapsedTime = 0
		finished = False
		p = subprocess.Popen('./glucose2.2/core/glucose ' + str(f), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
		while(p.poll() == None):
			if (elapsedTime > cutoff):
				break

			# Sleep and increment time...
			sleep(sleepInterval)
			elapsedTime = elapsedTime + sleepInterval

		if (p.poll() != None):
			finished = True
		if (finished):
			for line in p.stdout.readlines():
				if (line.startswith("CPU time")):
					data = line.split(" ")
					time = float(data[len(data) - 2]) # CPU _ Time _ : _ <time here>
					print >> sys.stderr, "Reported time: " + time
					times.append((f, time))
		else:
			os.killpg(p.pid, signal.SIGTERM)
			times.append((f, -1)) # -1 indicates unfinished run...

	# Display the result
	print(times)

