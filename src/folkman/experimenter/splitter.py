#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: splitter.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from reducer import reducer
from reducer import makeDimacsCNF
import sys
import argparse
import random
import time

# Heuristic:
# 1. 
#(random) split Nv = B union R with n(v) >= 154.
#2.
#Precolor the edges from v to Nv and those induced by B and R,
#as described above. This precolors 42 + about (231-154),
#or almost 120 edges.
#3.
#Make a SAT instance alpha for this precoloring.= GNR(127, 3)

G = GNR(127,3)
nv = 125 # THIS SHOULD BE 157 as per SPR's comments
print >> sys.stderr, "Searching for split"
v, bags, B, R, pcmap = G.find_candidate_rb_split(nv) 
print >> sys.stderr, str(B)
print >> sys.stderr, str(R)
print >> sys.stderr, "Passing to reducer with precoloring in place (bags)..."


#### OLD CODE BELOW
# Split into r/b coloring (two bags) and avoid K3 (triangle)
#print >> sys.stderr, "In line at the grocery store now (bagging)!"
#bags = G.random_edge_split_avoid_kn(2,3)
#bags = G.iterative_edge_split_avoid_kn(2,3)
#while bags == None:
#	print >> sys.stderr, "Trying again..."
#	bags = G.iterative_edge_split_avoid_kn(2,3)
#print >> sys.stderr, "Success!"

def timestampMilli(msg, start, end):
	print >> sys.stderr, msg + str((end - start) * 1000) + "ms"

def main():
	parser = argparse.ArgumentParser(prog='injector')
	#parser.add_argument('-n', type=int)
	#parser.add_argument('-r', type=int)
	#parser.add_argument('-sample_size', type=int, default=0)
	#parser.add_argument('-na', '--num_assigned', type=int, default=0)
	#parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
	#parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	#parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	#parser.add_argument('-nerr', type=int, default=0)
	#parser.add_argument('-s', '--seed', type=int)
	#parser.add_argument('-out', '--out_file', type=str, default="reducedCnf")
	#parser.add_argument('-smart',type=bool,default=False)
	#parser.add_argument('-saturate',type=bool,default=False)
	#parser.add_argument('-assign',type=bool,default=True)
	args = parser.parse_args()

	start = time.time()
	# DO THE SPLITTING HERE	
	end = time.time()
	timestampMilli("Total time: ", start, end)

if __name__ == "__main__":
	main()

