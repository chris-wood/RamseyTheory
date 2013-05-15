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

# Usage: python injector.py -n -r -sample -na -ne -pl -nrr -nerr -nisr 
# -n = n
# -r = r
# -sample = number of random variable configurations to choose from (enter 2^na to cover them all...)
# -na = number variables assigned
# -ne = number of edges to add to H
# -nrr = number of randomly removed vertices
# -nerr = number of edges randomly removed
# -nisr = number of maximum independent sets removed
# -out = out files for the CNFs

class injector:
	def __init__(self, n, r, sample, fix, na, smart, ne, nrr, nerr, nisr, out, dump):
		self.n = n
		self.r = r
		self.sample = sample
		self.graph = GNR(n, r)
		self.fix = fix
		self.na = na
		self.smart = smart
		self.ne = ne
		self.nrr = nrr
		self.nerr = nerr
		self.nisr = nisr
		self.out = out
		self.dump = dump

		# Preliminary error checking
		if (self.graph.getGraph().edges() < self.na):
			raise Exception("Cannot remove more edges than the graph contains.")
		if (n < (nrr + nisr)):
			raise Exception("Cannot remove more vertices than the graph contains.")

		# Generate the CNF formula
		# r = reducer()
		# print >> sys.stderr, 'Creating the original CNF formula'
		# numVars, cnf = r.reduce(self.graph.getGraph())
		# self.write("reduced", numVars, cnf, 0)

		# Strip down to the induced subgraph
		# using the structural/random properties, as specified
		# by the command cmd line arguments
		print >> sys.stderr, 'Stripping the graph'
		self.strip()
		print >> sys.stderr, 'Filling out edges'
		# edgesAdded = self.fill() # Let exceptions carry up to -main-

		# Saturate by default!
		self.graph.saturateAvoidK4();

		r = reducer()
		print >> sys.stderr, "Reducing to 3-SAT"
		numVars, cnf = r.reduce(self.graph.getGraph())
		self.write("reduced", numVars, cnf, 0)

		if (self.dump):
			print >> sys.stderr, "Dumping the modified graph"
			self.dumpGraph()

		# Assign values and propagate, if fix was set to true
		print >> sys.stderr, 'Assigning the random variables'
		if (self.fix):
			self.assignAndWrite(numVars, cnf)

	def dumpGraph(self):
		for e in self.graph.getGraph().edges():
			print(str(e[0]) + " " + str(e[1]))

	def strip(self):
		for i in range(self.nrr):
			node = random.randint(0, self.n)
			self.graph.dropNode(node)
			self.n = self.n - 1
		for i in range(self.nisr):
			self.graph.removeIndependentSet()
		for i in range(self.nerr):
			edge = random.randint(0, len(self.graph.getGraph().edges()))
			self.graph.dropEdge(edge)

	def fill(self):
		edgesAdded = 0
		for i in range(self.ne):
			if self.graph.addRandomEdgeAvoidK4():
				edgesAdded = edgesAdded + 1
		return edgesAdded


	def edgesIntersect(self, e, vars, cnf):
		for c in cnf:
			for v in vars:
				if (v in c) and (e in c):
					return True
		return False

	def assignAndWrite(self, numVars, cnf):
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
		if (self.smart):
			loop = 0
			THRESHOlD = 100 # There has to be a way to determine the maximum number of disjoint things...
			for i in range(self.na):
				if loop > THRESHOlD:
					break
				else:
					var = random.randint(0, numVars)
					loop = 0
					while (self.edgesIntersect(var, varsToAssign, cnf) and loop < THRESHOlD):
						loop = loop + 1
						var = random.randint(0, numVars)
					if (loop < THRESHOlD):
						varsToAssign.append(var)
		else:
			for i in range(self.na):
				var = random.randint(0, numVars)
				if (var not in varsToAssign):
					varsToAssign.append(var)
				else:
					while (var in varsToAssign):
						var = random.randint(0, numVars)
					varsToAssign.append(var)

		print >> sys.stderr, "Variables to assign: " + str(varsToAssign)

		# list of all possible variable assignments, start with all false
		assign = {}
		for i in range(self.na):
			assign[varsToAssign[i]] = False
		print >> sys.stderr, "Assigning variables..."

		configSamples = []
		configIndex = 0
		#for config in range(2 ** self.na):
		numSamples = 2 ** self.na
		while (configIndex < self.sample or numFormulas == 0):

			# Select a random configuration not already in the set
			c = random.randint(0, numSamples)
			while (c in configSamples):
				c = random.randint(0, numSamples)
			configSamples.append(c)
			
			# Advance the configuration array...
			for i in range(len(assign.keys())):
				if (((1 << i) & c) > 0):
					assign[assign.keys()[i]] = True
				else:
					assign[assign.keys()[i]] = False

			# Print out the configuration we're on...
			if (configIndex % 500 == 0):
				print >> sys.stderr, "Config " + str(configIndex)
			newCnf = []
			for c in cnf: # for each clause
				include = True
				clause = c[:] # Copy over the clause
				settled = False
				# print("Examining clause: " + str(clause))
				for l in c: # for each literal
					if include and settled == False:
						index = -1
						inVars = False
						negative = False
						if (l < 0 and (l * -1) in varsToAssign):
							index = (l * -1)
							inVars = True
							negative = True
						elif (l > 1 and l in varsToAssign):
							index = l
							inVars = True
						if inVars:
							settled = True
							if (assign[index] == True and negative == False): # the literal is true, so drop the clause
								# print("Dropping clause because " + str(index) + " was assigned to " + str(assign[index]))
								include = False
							elif (assign[index] == True and negative == True):
								# print("Dropping literal " + str(index) + " from the clause because it was assigned to " + str(assign[index]))
								include = True
								clause.remove(l) # remove the literal, it evaluated to false...
							elif (assign[index] == False and negative == False):
								# print("Dropping literal " + str(index) + " from the clause because it was assigned to " + str(assign[index]))
								include = True
								clause.remove(l) # remove the literal, it evaluated to false...
							elif (assign[index] == False and negative == True):
								# print("Dropping clause because " + str(index) + " was assigned to " + str(assign[index]))
								include = False
				if include:
					# print("Resulting clause inserted: " + str(clause))
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
						elif (l > 0 and l in units.keys()):
							index = l
							inVars = True
						if inVars:
							if (units[index] == True): # the literal is true, so drop the clauses
								include = False
								print >> sys.stderr, "HOW CAN THIS HAPPEN?"
								return 
							else:
								clause.remove(l) # remove the literal, it evaluated to false...
				if include and len(clause) > 0: # do not append empty clauses, they cause immediate unsatisfiability...
					if (len(clause) == 2):
						sizeTwoClauses = sizeTwoClauses + 1
					elif (len(clause) == 3):
						sizeThreeClauses = sizeThreeClauses + 1
					finalCnf.append(clause)
				elif (len(clause) == 0):
					# print >> sys.stderr, "Found unsatisfiable clause in variable configuration " + str(configIndex) + ", discarding formula."
					write = False
					break

			configIndex = configIndex + 1

			# Write the output file
			if (write):
				# Compound total number of formulas
				numFormulas = numFormulas + 1
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
				totalRatio = totalRatio + (float(totalTwoClauses) / float(totalThreeClauses))

		# Output the stats (if we actually wrote anything...)
		if (numFormulas > 0):
			print >> sys.stderr, "Total number of formulas: " + str(numFormulas)
			print >> sys.stderr, "Minimum number of 2-clauses: " + str(minTwoClauses)
			print >> sys.stderr, "Maximum number of 2-clauses: " + str(maxTwoClauses)
			print >> sys.stderr, "Average number of 2-clauses: " + str(totalTwoClauses / numFormulas)
			print >> sys.stderr, "Minimum number of 3-clauses: " + str(minThreeClauses)
			print >> sys.stderr, "Maximum number of 3-clauses: " + str(maxThreeClauses)
			print >> sys.stderr, "Average number of 3-clauses: " + str(totalThreeClauses / numFormulas)
			print >> sys.stderr, "Average ratio of 2-to-3 clauses: " + str(totalRatio / numFormulas)

	def write(self, index, numVars, cnf, numTwoClauses):
		print >> sys.stderr, str(self.out + "_" + str(index))
		f = open(self.out + "_" + str(index), 'wb')
		header, clauses = makeDimacsCNF(numVars, cnf)
		f.write('c ' + str(numTwoClauses) + "\n")
		f.write(header + "\n")
		for c in clauses:
			for l in c:
				f.write(str(l) + " ")
			f.write("0 \n")

def showUsage():
	print >> sys.stderr, "Usage: python injector.py [args]"
	print >> sys.stderr, "  -n = num vertices in G(n,r) (REQUIRED)"
	print >> sys.stderr, "  -r = r in G(n,r) (REQUIRED)"
	print >> sys.stderr, "  -sample = number of random variable configurations to choose from (enter 2^na to cover them all...)"
	print >> sys.stderr, "  -na = number variables assigned"
	print >> sys.stderr, "  -ne = number of edges to add to H"
	print >> sys.stderr, "  -nrr = number of randomly removed vertices"
	print >> sys.stderr, "  -nerr = number of edges randomly removed"
	print >> sys.stderr, "  -nisr = number of maximum independent sets removed"
	print >> sys.stderr, "  -out = out files for the CNFs"

def timestampMilli(msg, start, end):
	print >> sys.stderr, msg + str((end - start) * 1000) + "ms"

def main():
	parser = argparse.ArgumentParser(prog='injector')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-sample', type=int, default=0)
	parser.add_argument('-na', '--num_assigned', type=int, default=0)
	parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
	parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	parser.add_argument('-nerr', type=int, default=0)
	parser.add_argument('-s', '--seed', type=int)
	parser.add_argument('-out', '--out_file', type=str, default="reducedCnf")
	parser.add_argument('-smart',type=bool,default=False)
	parser.add_argument('-fix',type=bool,default=True)
	parser.add_argument('-dump',type=bool,default=False)
	args = parser.parse_args()

	# Check the command line arguments first...
	if (args.n == None or args.r == None):
		showUsage()
		return -1
	else:
		n = args.n
		r = args.r
		sample = args.sample
		na = args.num_assigned
		ne = args.num_edges_to_add
		nrr = args.number_random_removed
		nerr = args.nerr
		nisr = args.number_independet_sets_removed
		seed = args.seed
		out = args.out_file
		smart = args.smart
		fix = args.fix
		dump = args.dump

		# Seed random...
		random.seed(seed)

		# Create the injector...
		#try:
		start = time.time()
		inject = injector(n, r, sample, fix, na, smart, ne, nrr, nerr, nisr, out, dump)
		end = time.time()
		timestampMilli("Total time: ", start, end)
		#except Exception as e:
		#	print >> sys.stderr, "\nError: " + str(e) + "\n"
		#	showUsage()
		#	return -1

if __name__ == "__main__":
	main()

