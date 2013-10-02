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

def triangle_type(G, v, v1, v2, v3, B, R, T):

	v1b = v1 in B
	v2b = v2 in B
	v3b = v3 in B
	v1r = v1 in R
	v2r = v2 in R
	v3r = v3 in R
	v1t = v1 in T
	v2t = v2 in T
	v3t = v3 in T

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
		elif pair[0] in B and pair[1] in B:
			return 2
		elif pair[0] in R and pair[1] in R:
			return 3
		else:
			raise Exception("Not possible HOMER! Check the (1/2/3) categorization code.")
	elif v1b or v2b or v3b: # cases 4/6/7
		if (v1b and v2b) or (v1b and v3b) or (v2b and v3b):
			return 4
		elif v1r or v2r or v3r: # 1 in b and 1 in r, the third must be in T
			return 6
		elif (v1t and v2t) or (v1t and v3t) or (v2t and v3t):
			return 7
		else:
			raise Exception("Not possible HOMER! Check the (4/6/7) categorization code.")
	elif v1r or v2r or v3r: # cases 5/8
		if (v1r and v2r) or (v1r and v3r) or (v2r and v3r):
			return 5
		elif v1r or v2r or v3r: # 1 in b and 1 in r, the third must be in T
			return 6 # duplicate case as above!
		elif (v1t and v2t) or (v1t and v3t) or (v2t and v3t):
			return 8
		else:
			raise Exception("Not possible HOMER! Check the (4/6/7) categorization code.")
	elif v1t and v2t and v3t: # case 9
		return 9
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
v, bags, B, R, T, pcmap = G.find_candidate_rb_split(nv, target = 21, delta = 0.9) 
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

# def timestampMilli(msg, start, end):
# 	print >> sys.stderr, msg + str((end - start) * 1000) + "ms"

# def main():
# 	parser = argparse.ArgumentParser(prog='injector')
# 	#parser.add_argument('-n', type=int)
# 	#parser.add_argument('-r', type=int)
# 	#parser.add_argument('-sample_size', type=int, default=0)
# 	#parser.add_argument('-na', '--num_assigned', type=int, default=0)
# 	#parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
# 	#parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
# 	#parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
# 	#parser.add_argument('-nerr', type=int, default=0)
# 	#parser.add_argument('-s', '--seed', type=int)
# 	#parser.add_argument('-out', '--out_file', type=str, default="reducedCnf")
# 	#parser.add_argument('-smart',type=bool,default=False)
# 	#parser.add_argument('-saturate',type=bool,default=False)
# 	#parser.add_argument('-assign',type=bool,default=True)
# 	args = parser.parse_args()

# 	start = time.time()
# 	# DO THE SPLITTING HERE	
# 	end = time.time()
# 	timestampMilli("Total time: ", start, end)

# if __name__ == "__main__":
	# main()

