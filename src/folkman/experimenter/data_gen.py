import sys
import subprocess
import os
import shutil
import glob

# Read in params from cmd line
trials = int(sys.argv[1])
seed = int(sys.argv[2])
smart = int(sys.argv[3])
params = sys.argv[4]

# Read in graph adjustment params from file
with open(params, 'r') as f:
	nrr = f.readline().strip().split(",")
	nisr = f.readline().strip().split(",")
	na = f.readline().strip().split(",")


# Perform each combination...

# TODO: insert traversal of combinations here

p = subprocess.Popen('java -classpath pj.jar:. ParallelL21Assignment 2 ' + str(low) + ' ' + str(high) + " " + fname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
lines = []
for l in p.stdout.readlines():
	l = l.strip()
	lines.append(l)
fout = open(fname + ".span", 'w')
for l in lines:
	print >> sys.stderr, l
	print(l)
	fout.write(l + "\n")



