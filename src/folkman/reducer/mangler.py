#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: mangler.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from reducer import reducer
from reducer import makeDimacsCNF
import sys
import argparse
import random
import time

# Usage: python mangler.py -n -r -na -ne -pl -nrr -nisr 
# -n = n
# -r = r
# -na = number variables assigned
# -ne = number of edges to add to H
# -pl = variable propagation levels
# -nrr = number of randomly removed vertices
# -nisr = number of maximum independent sets removed
# -out = out files for the CNFs

class mangler:
	def __init__(self, n, r, na, ne, pl, nrr, nisr, out):
		self.n = n
		self.r = r
		self.graph = GNR(n, r)
		self.na = na
		self.ne = ne
		self.pl = pl
		self.nrr = nrr
		self.nisr = nisr
		self.out = out

		# Start down to the induced subgraph
		self.strip()

		# Generate the CNF formula
		r = reducer()
		print >> sys.stderr, 'Creating the CNF formula'
		numVars, cnf = r.reduce(self.graph.getGraph())

		# Assign values and propagate
		print >> sys.stderr, 'Assigning the random variables'
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
		for i in range(self.na):
			var = random.randint(0, numVars)
			if (var not in varsToAssign):
				varsToAssign.append(var)
			else:
				while (var in varsToAssign):
					var = random.randint(0, numVars)
				varsToAssign.append(var)

		# list of all possible variable assignments, start with all false
		assign = {}
		for i in range(self.na):
			assign[varsToAssign[i]] = False
		print("Assigning variables...")

		configIndex = 0
		for config in range(2 ** self.na):
			print("Config " + str(configIndex))
			newCnf = []
			for c in cnf: # for each clause
				include = True
				clause = c[:] # Copy over the clause
				for l in c: # for each literal
					if include:
						index = -1
						inVars = False
						if (l < 0 and (l * -1) in varsToAssign):
							index = (l * -1)
							inVars = True
						elif (l > 1 and l in varsToAssign):
							index = l
							inVars = True
						if inVars:
							if (assign[index] == True): # the literal is true, so drop the clauses
								include = False
							else:
								clause.remove(l) # remove the literal, it evaluated to false...
				if include:
					newCnf.append(clause)

			# Pass over the new CNF and find all unit clauses
			# This is for unit propagation...
			units = {}
			for c in newCnf:
				if (len(c) == 1):
					literal = c[0]
					if (literal < 0):
						units[literal * -1] = False
						# unitAssigns.append(False) # must be false
					else:
						units[literal] = True
						# unitAssigns.append(True)
			# Now that we have all of the unit literals with their truth values, perform the walk again...
			finalCnf = []

			# compute average time for each of the results
			# multiply by 2^20 for hardness!

			# TODO: Make this into a method? (oldCnf, variable list with assignments, ...)

			sizeTwoClauses = 0
			for c in newCnf: # for each clause
				include = True
				clause = c[:] # Copy over the clause
				for l in c: # for each literal
					if include:
						index = -1
						inVars = False
						if (l < 0 and (l * -1) in units.keys()):
							index = (l * -1)
							inVars = True
						elif (l > 1 and l in units.keys()):
							index = l
							inVars = True
						if inVars:
							if (units[index] == True): # the literal is true, so drop the clauses
								include = False
							else:
								clause.remove(l) # remove the literal, it evaluated to false...
				if include and len(clause) > 0: # do not append empty clauses, they cause immediate unsatisfiability...
					if (len(clause) == 2):
						sizeTwoClauses = sizeTwoClauses + 1
					finalCnf.append(clause)
				elif (len(clause) == 0):
					print("Found unsatisfiable clause in variable configuration " + str(configIndex) + ", discarding formula.")

			# Write the output file
			self.write(configIndex, numVars, finalCnf, sizeTwoClauses)
			configIndex = configIndex + 1

			# advance the configuration
			for k in assign.keys():
				if (assign[k] == True): # propagate to the next clause!
					assign[k] = False
				else:
					assign[k] = True
					break # hop out early...

	def write(self, index, numVars, cnf, numTwoClauses):
		print("Writing: " + str(self.out + "_" + str(index)))
		f = open(self.out + "_" + str(index), 'wb')
		header, clauses = makeDimacsCNF(numVars, cnf)
		f.write('c ' + str(numTwoClauses) + "\n")
		f.write(header + "\n")
		for c in clauses:
			for l in c:
				f.write(str(l) + " ")
			f.write("0 \n")

def timestampMilli(msg, start, end):
	print(msg + str((end - start) * 1000) + "ms")

def main():
	parser = argparse.ArgumentParser(prog='mangler')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-na', '--num_assigned', type=int, default=0)
	parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
	parser.add_argument('-pl', '--propagation_level', type=int, default=1)
	parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	parser.add_argument('-s', '--seed', type=int)
	parser.add_argument('-out', '--out_file', type=str, default="reducedCnf")
	args = parser.parse_args()
	print(args)

	# Check the command line arguments first...
	if (args.n == None or args.r == None):
		print("Error: n and r are required.")
	else:
		n = args.n
		r = args.r
		na = args.num_assigned
		ne = args.num_edges_to_add
		pl = args.propagation_level
		nrr = args.number_random_removed
		nisr = args.number_independet_sets_removed
		seed = args.seed
		out = args.out_file

		# Seed random...
		random.seed(seed)

		# Create the injector...
		start = time.time()
		inject = injector(n, r, na, ne, pl, nrr, nisr, out)
		end = time.time()
		timestampMilli("Total time: ", start, end)

if __name__ == "__main__":
	main()

