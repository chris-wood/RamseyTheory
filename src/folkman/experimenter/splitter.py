#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: splitter.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from injector import *
from reducer import reducer
from reducer import makeDimacsCNF
import sys
import argparse
import random
import time

def medge(v1, v2):
	if v1 <= v2:
		return (v1, v2)
	else:
		return (v2, v1)

def triangle_type(G, v, v1, v2, v3, B, R):
	if v == v1 or v == v2 or v == v3: # cases 1/2/3
		tv = v1
		pair = (v2, v3)
		if v == v2:
			tv = v2
			pair = (v1, v3)
		else:
			tv = v3
			pair = (v1, v2)

		# differentiate the cases
		if pair[0] in B and pair[1] in B:
			return 1
		if pair[0] in B and pair[1] in B:
			return 2
		else if pair[0] in R and pair[1] in R:
			return 3

	elif v1 in B or v2 in B or v3 in B: # cases 4/6/7

		# TODO: continue here

		return 0
	else:
		raise Exception("Not possible HOMER! Check the categorization code.")

def define_triangle_classes(G, v, B, R, pcmap):
	counts = []
	for i in range(9): # there are 9 classes per SPR's comments
		counts.append(0)

	# Exhaustively search for all triangles and then switch on what type they are
	# and throw them into the right count bucket
	triangles = 0
	for v1 in G.nodes():
		for v2 in G.nodes():
			for v3 in G.nodes():
				if (medge(v1, v2) in G.edges() and medge(v1, v3) in G.edges() and medge(v2, v3) in G.edges()):
					triangles = triangles + 1

					# TODO: do the classification of the triangle here.. put the tuple in the appropriate bucket


	return triangles

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

nv = int(sys.argv[1]) # THIS SHOULD BE 157 as per SPR's comments
print >> sys.stderr, "Searching for split"
start = time.time()
v, bags, B, R, pcmap = G.find_candidate_rb_split(nv, target = 21, delta = 0.9) 
end = time.time()
print >> sys.stdout, str((end - start) * 1000) + "ms"
print >> sys.stderr, str((end - start) * 1000) + "ms"
print >> sys.stdout, str(v)
print >> sys.stdout, str(B)
print >> sys.stdout, str(R)
print >> sys.stderr, str(v)
print >> sys.stderr, str(B)
print >> sys.stderr, str(R)
print >> sys.stderr, "Split found!"


# Do the SAT conversion later
#injector = injector()
#injector.inject_arbitrary_graph_with_edge_precoloring(G, pcmap)

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

