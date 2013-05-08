#!/usr/bin/python

#
# File: AutomateTreeCheck.py
# Author: Christopher A. Wood, caw4567@rit.edu
# Description: TODO
#

import sys
import subprocess
import os
import shutil

if (len(sys.argv) != 1):
	print "Usage: python experiment.py fileList"
else:
	inputFile = sys.argv[1]
	files = open(inputFile, 'r')
	times = []

	sleepInterval = 5
	cutoff = 1800

	for f in files:
		print >> sys.stderr, "Running: " + file
		elapsedTime = 0
		finished = False
		p = subprocess.Popen('python ' + alg + ' ' + samples + '/' + file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		while(p.poll() == None):
			if (elapsedTime > cutoff):
				break

			# Sleep and increment time...
			sleep(sleepInterval)
			elapsedTime = elapsedTime + sleepInterval

		if (finished):
			for line in p.stdout.readlines():
				if (line.startswith("CPU time")):
					data = line.split(" ")
					time = float(data[len(data) - 2]) # CPU _ Time _ : _ <time here>
					print >> sys.stderr, "Reported time: " + time
					times.append((f, time))
		else:
			p.kill() # kill it...
			times.append((f, -1)) # -1 indicates unfinished run...

	# Display the result
	print(times)
	
	# # Grab all files...
	# listing = os.listdir(samples)
	# print("Running from " + samples)
	# for file in listing:
		
	# 	# Get the extension and check it
	# 	fileName, fileExtension = os.path.splitext(file)
	# 	if (fileExtension == '.cnf'): # yeah, don't forget this... >.<
			
	# 		# Run the L21 algorithm on all samples
	# 		print "Running: " + file
	# 		p = subprocess.Popen('python ' + alg + ' ' + samples + '/' + file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# 		sleep(1800) # 30 minutes!
	# 		testPass = True
	# 		for line in p.stdout.readlines():
	# 			try:
	# 				if ("true" in line):
	# 					testPass = False # it had the property, so test failed
	# 			except:
	# 				raise Exception("Something went wrong with file: " + str(file))
	# 				#testPass = False
			
	# 		# Copy the file over to the correct location for continual or manual inspection
	# 		if (testPass == True):
	# 			print("Passed (doesn't contain the forbidden subtree)")
	# 			print("saving to  " + str(passDir + '/' + file))
	# 			shutil.copy2(samples + '/' + file, passDir + '/' + file)
	# 		else:
	# 			print("Failed (contains the forbidden subtree)")
	# 			print("saving to  " + str(failDir + '/' + file))
	# 			shutil.copy2(samples + '/' + file, failDir + '/' + file)
