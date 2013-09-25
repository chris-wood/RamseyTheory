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
# 1. find a coloring without monochromatic triangles
# 2. pick a random vertex in the graph
# 3. Let N(v) (neighboring nodes) is the union of nodes connected via B(lue) edges and R(ed) edges
# 4. Compute n(v), the number of edges between B and R
# 5. If n(v) >= 154, generate SAT equivalent for the coloring and write to disk, try to solve

# Build G
G = GNR(127, 3)

# Split into r/b coloring (two bags) and avoid K3 (triangle)
print >> sys.stderr, "In line at the grocery store now (bagging)!"
#bags = G.random_edge_split_avoid_kn(2,3)
bags = G.iterative_edge_split_avoid_kn(2,3)
print >> sys.stderr, "Success!"

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

