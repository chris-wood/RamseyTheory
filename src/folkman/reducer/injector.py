#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: injector.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from reducer import reducer
from reducer import makeDimacsCNF
import sys
import argparse
import random
import time

# Usage: python injector.py -n -r -na -ne -pl -nrr -nisr 
# -n = n
# -r = r
# -sample = number of random variable configurations to choose from (enter 2^na to cover them all...)
# -na = number variables assigned
# -ne = number of edges to add to H
# -pl = variable propagation levels
# -nrr = number of randomly removed vertices
# -nerr = number of edges randomly removed
# -nisr = number of maximum independent sets removed
# -out = out files for the CNFs

class injector:
	def __init__(self, n, r, sample, na, ne, pl, nrr, nerr, nisr, out):
		self.n = n
		self.r = r
		self.sample = sample
		self.graph = GNR(n, r)
		self.na = na
		self.ne = ne
		self.pl = pl
		self.nrr = nrr
		self.nerr = nerr
		self.nisr = nisr
		self.out = out

		# Generate the CNF formula
		r = reducer()
		print >> sys.stderr, 'Creating the original CNF formula'
		numVars, cnf = r.reduce(self.graph.getGraph())
		self.write("reduced", numVars, cnf, 0)

		# Strip down to the induced subgraph
		# using the structural/random properties, as specified
		# by the command cmd line arguments
		print >> sys.stderr, 'Creating the reduced CNF formula'
		self.strip()
		r = reducer()
		numVars, cnf = r.reduce(self.graph.getGraph())
		self.write("reduced", numVars, cnf, 0)

		# Assign values and propagate
		print >> sys.stderr, 'Assigning the random variables'
		self.assignAndWrite(numVars, cnf)

	def strip(self):
		for i in range(self.nrr):
			node = random.randint(0, self.n)
			self.graph.dropNode(node)
			self.n = self.n - 1
		for i in range(self.nisr):
			self.graph.removeIndependentSet()
		for i in range(self.nerr):
			edge = random.randint(0, len(self.graph.getGraph().edges()))

	def assignAndWrite(self, numVars, cnf):
		# Statistic vars
		numClauses = len(cnf)
		numFormulas = 0
		minTwoClauses = numClauses
		totalTwoClauses = 0
		maxTwoClauses = 0
		minThreeClauses = numClauses
		maxThreeClauses = 0
		totalThreeClauses = 0
		totalRatio = 0

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

		configSamples = []
		configIndex = 0
		#for config in range(2 ** self.na):
		numSamples = 2 ** self.na
		while (configIndex < self.sample):

			# Select a random configuration not already in the set
			c = random.randint(0, numSamples)
			while (c in configSamples):
				c = random.randint(0, numSamples)
			configSamples.append(c)

			# Initialize the configuration array
			for i in range(len(assign.keys())):
				if (((1 << i) & c) > 0):
					assign[assign.keys()[i]] = True
				else:
					assign[assign.keys()[i]] = False

			# Print out the configuration we're on...
			print >> sys.stderr, "Config " + str(configIndex)
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
					else:
						units[literal] = True
			# Now that we have all of the unit literals with their truth values, perform the walk again...
			finalCnf = []

			sizeTwoClauses = 0
			sizeThreeClauses = 0
			write = True
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
					elif (len(clause) == 3):
						sizeThreeClauses = sizeThreeClauses + 1
					finalCnf.append(clause)
				elif (len(clause) == 0):
					print("Found unsatisfiable clause in variable configuration " + str(configIndex) + ", discarding formula.")
					write = False

			configIndex = configIndex + 1

			# Write the output file
			if (write):
				self.write(configIndex, numVars, finalCnf, sizeTwoClauses)

				# Compound the statistics for the two clauses
				if (sizeTwoClauses < minTwoClauses):
					minTwoClauses = sizeTwoClauses
				if (sizeTwoClauses > maxTwoClauses):
					maxTwoClauses = sizeTwoClauses
				totalTwoClauses = totalTwoClauses + sizeTwoClauses

				# Compound stats for three clauses
				if (sizeThreeClauses < minThreeClauses):
					minThreeClauses = sizeThreeClauses
				if (sizeThreeClauses > maxThreeClauses):
					maxThreeClauses = sizeThreeClauses
				totalThreeClauses = totalThreeClauses + sizeThreeClauses

				# Compound ratio
				totalRatio = totalRatio + (float(totalTwoClauses) / float(totalThreeClausess))

				# Compound total number of formulas
				numFormulas = numFormulas + 1

		# Output the stats (if we actually wrote anything...)
		if (numFormulas > 0):
			print("Total number of formulas: " + str(numFormulas))
			print("Minimum number of 2-clauses: " + str(minTwoClauses))
			print("Maximum number of 2-clauses: " + str(maxTwoClauses))
			print("Average number of 2-clauses: " + str(totalTwoClauses / numFormulas))
			print("Minimum number of 3-clauses: " + str(minThreeClauses))
			print("Maximum number of 3-clauses: " + str(maxThreeClauses))
			print("Average number of 3-clauses: " + str(totalThreeClauses / numFormulas))
			print("Average ratio of 2-to-3 clauses: " + str(totalRatio / numFormulas))

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
	parser = argparse.ArgumentParser(prog='injector')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-sample', type=int, default=100)
	parser.add_argument('-na', '--num_assigned', type=int, default=0)
	parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
	parser.add_argument('-pl', '--propagation_level', type=int, default=1)
	parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	parser.add_argument('-nerr', type=int, default=0)
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
		sample = args.sample
		na = args.num_assigned
		ne = args.num_edges_to_add
		pl = args.propagation_level
		nrr = args.number_random_removed
		nerr = args.nerr
		nisr = args.number_independet_sets_removed
		seed = args.seed
		out = args.out_file

		# Seed random...
		random.seed(seed)

		# Create the injector...
		start = time.time()
		inject = injector(n, r, sample, na, ne, pl, nrr, nerr, nisr, out)
		end = time.time()
		timestampMilli("Total time: ", start, end)

if __name__ == "__main__":
	main()

