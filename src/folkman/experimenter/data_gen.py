import sys
import subprocess
import os
import shutil
import glob

# Read in params from cmd line
trials = int(sys.argv[1])
seed = int(sys.argv[2])
params = sys.argv[3]

# Read in graph adjustment params from file
nrrList = []
nisrList = []
naList = []
neList = []
smartList = [False]
saturateList = [False]

# G127 params
n = 127
r = 3

with open(params, 'r') as f:
	nrrList = f.readline().strip().split(",")
	nisrList = f.readline().strip().split(",")
	naList = f.readline().strip().split(",")
	neList = f.readline().strip().split(",")

for t in range(trials):
	for nrr in nrrList:
		for nisr in nisrList:
			for na in naList:
				for ne in neList:
					for smart in smartList:
						for saturate in saturateList:
							prefix = str(n) + "_" + str(r) + "_" + str(nrr) + "_" + str(nisr) + "_" + str(na)
							directory = os.path.dirname(os.path.abspath(__file__)) + prefix + os.pathsep
							if not os.path.exists(directory):
								os.makedirs(directory)
							runCmd = "python injector.py -n " + str(n) + " -r " + str(r) + " -na " + str(na) + " -ne " + str(ne) + " -nrr " + str(nrr) + " -nisr " + str(nisr) + " -out " + prefix + " -s " + str(seed) + " -smart " + str(smart) + " -saturate " + str(saturate)
							print >> sys.stderr, "Running: " + runCmd
							p = subprocess.Popen(runCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
					
							# Capture and record the output
							fname = directory + prefix + "_" + str(t) + ".cnf"
							lines = []
							for l in p.stdout.readlines():
								l = l.strip()
								lines.append(l)
							fout = open(fname, 'w')
							for l in lines:
								print >> sys.stderr, l
								print(l)
								fout.write(l + "\n")

