import sys
import os

contents = []
c5permutations = open('c5permutations.mat', 'w')
index = 1
for dirpath, dnames, fnames in os.walk("./"):
    for fName in fnames:
        if fName.endswith(".txt") and fName.startswith("m"):
        	f = open(fName, 'r')
        	c5permutations.write("Permutation " + str(index) + "\n")
        	for line in f:
        		c5permutations.write(line)
        	c5permutations.write('\n\n')
        	index = index + 1