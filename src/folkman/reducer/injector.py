#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: injector.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from reducer import reducer
import sys
import argparse
import random

# Usage: python injector.py -n -r -na -pl -nrr -nisr 
# -n = n
# -r = r
# -na = number variables assigned
# -pl = variable propagation levels
# -nrr = number of randomly removed vertices
# -nisr = number of maximum independent sets removed

class injector:
	def __init__(self, n, r, na, pl, nrr, nisr):
		self.n = n
		self.r = r
		self.graph = GNR(n, r)
		self.na = na
		self.pl = pl
		self.nrr = nrr
		self.nisr = nisr

		# Start stripping...
		self.strip()

		# Generate the CNF formula
		r = reducer()
		numVars, cnf = r.reduce(self.graph.getGraph())

		# Assign values and propagate
		self.assignValues(numVars, cnf)

	def strip(self):
		for i in range(self.nrr):
			node = random.randint(0, self.n)
			self.graph.dropNode(node)
			self.n = self.n - 1
		for i in range(self.nisr):
			self.graph.removeIndependentSet()

	def assignValues(self, numVars, cnf):
		# list of random variables to remove
		varsToAssign = []
		for i in range(sekf.na):
			var = random.randint(0, numVars)
			if (var not in varsToAssign):
				varsToAssign.append(var)

		# list of all possible variable assignments, start with all false
		assign = [] 
		for i in range(numVars):
			assign.append(False)

		for config in range(2 ** numVars):
			newCnf = []
			for i in range(self.pl):
				for c in cnf: # for each clause
					isTrue = False
					for l in c: # for each literal
						if (l < 0 and (l * -1) in vars and assign[(l * -1) - 1] == True):
							isTrue = True
						elif (l > 0 and l in vars and assign[(l * -1) - 1] == True):
							isTrue = True
					if not isTrue:
						newCnf.append(c)

			# TODO: pick  a random variable
			# do two different assignments (true and false)
			# node: there will be 2^na resulting variables

	def propagate(self, numVars, cnf):
		raise Exception("NOT IMPLEMENTED")

def main():
	parser = argparse.ArgumentParser(prog='injector')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-na', '--num_assigned', type=int, default=0)
	parser.add_argument('-pl', '--propagation_level', type=int, default=1)
	parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	parser.add_argument('-s', '--seed', type=int)
	args = parser.parse_args()
	print(args)

	# Check the command line arguments first...
	if (args.n == None or args.r == None):
		print("Error: n and r are required.")
	else:
		n = args.n
		r = args.r
		na = args.num_assigned
		pl = args.propagation_level
		nrr = args.number_random_removed
		nisr = args.number_independet_sets_removed
		seed = args.seed

		# Seed random...
		random.seed(seed)

		# Create the injector...
		inject = injector(n, r, na, pl, nrr, nisr)

if __name__ == "__main__":
	main()

