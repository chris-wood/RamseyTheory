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
	def __init__(self, n, r, fix, sample_size, na, smart, saturate, ne, nrr, nerr, nisr, out):
		self.n = n
		self.r = r
		self.sample = sample_size
		self.graph = GNR(n, r)
		self.fix = fix
		self.na = na
		self.smart = smart
		self.saturate = saturate
		self.ne = ne
		self.nrr = nrr
		self.nerr = nerr
		self.nisr = nisr
		self.out = out

		# Preliminary error checking
		if (self.graph.getGraph().edges() < self.na):
			raise Exception("Cannot remove more edges than the graph contains.")
		if (n < (nrr + nisr)):
			raise Exception("Cannot remove more vertices than the graph contains.")
		
		# Strip down to the induced subgraph
		# using the structural/random properties, as specified
		# by the command cmd line arguments
		print >> sys.stderr, 'Stripping the graph...'
		print >> sys.stderr, "Random vertices to remove: " + str(nrr)
		print >> sys.stderr, "Random edges to remove: " + str(nerr)
		print >> sys.stderr, "Maximal independent sets to remove: " + str(nisr)
		self.strip()
		print >> sys.stderr, 'Done.'

		# Saturate by default!
		if (saturate):
			print >> sys.stderr, "Saturating with edges..."
			self.graph.saturateAvoidK4();
			print >> sys.stderr, "Done."

		# Now reduce the graph to 
		r = reducer()
		print >> sys.stderr, "Reducing to 3-SAT..."
		numVars, cnf = r.reduce(self.graph.getGraph())
		print >> sys.stderr, "Done."

		# Output or not...
		print >> sys.stderr, "Writing the original CNF formula..."
		self.write("reduce", numVars, cnf, 0)
		print >> sys.stderr, "Done."
		print >> sys.stderr, "Writing reduced graph edge list..."
		self.dumpGraph()
		print >> sys.stderr, "Done."

		# Assign values and propagate, if fix was set to true
		if (self.fix):
			print >> sys.stderr, "Performing edge assignment and writing the output..."
			self.assignAndWrite(numVars, cnf)
			print >> sys.stderr, "Done."

	# Write the edge-list representation of the graph (after preprocessed)
	# as well as the pickled graph object
	def dumpGraph(self):
		filename = self.out + "_graph.pickle"
		self.graph.dump(filename)
		for e in self.graph.getGraph().edges():
			print(str(e[0]) + " " + str(e[1]))

	# Strip down the graph according to the specified parameters
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

	# Fill in the graph with the parameters specificed
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

	def pickRandomEdgeToAssign(varsToAssign, numVars):
		var = random.randint(0, numVars)
		if (var in varsToAssign):
			while (var in varsToAssign):
				var = random.randint(0, numVars)
		return var

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

		# Pick the set of edges to assign
		# Smart selection of edges picks those that are disjoint (well, it tries to THRESHOLD times),
		#   and then it gives up and just picks a random one
		# "Dumb" selection just picks random edges, not caring whether or not they are disjoint
		varsToAssign = []
		if (self.smart):
			loop = 0
			THRESHOLD = 100 # There has to be a way to determine the maximum number of disjoint things...
			for i in range(self.na):
				if loop > THRESHOLD:
					break
				else:
					var = random.randint(0, numVars)
					loop = 0
					while (self.edgesIntersect(var, varsToAssign, cnf) and loop < THRESHOLD):
						loop = loop + 1
						var = random.randint(0, numVars)
					if (loop < THRESHOLD): # We found a disjoint one...
						varsToAssign.append(var)
					else: # Failed to find a disjoint one, so pick something at random
						varsToAssign.append(pickRandomEdgeToAssign(varsToAssign, numVars))
						
		else:
			for i in range(self.na):
				varsToAssign.append(pickRandomEdgeToAssign(varsToAssign, numVars))

		# debug
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
			# Now that we have all of the unit literals with their truth values, perform the walk again and do the substitution 
			# where we either remove clauses that evaluate to true or discard variables from clauses if the variable is false
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
							if (units[index] == True): # the literal is true, so drop the clause
								include = False
							else: # the literal is false, so remove the variable from the clause
								clause.remove(l) # remove the literal, it evaluated to false...
				# Do not append empty clauses, they cause immediate unsatisfiability...
				if include and len(clause) > 0:
 					if (len(clause) == 2):
						sizeTwoClauses = sizeTwoClauses + 1
					elif (len(clause) == 3):
						sizeThreeClauses = sizeThreeClauses + 1
					finalCnf.append(clause)
				elif (len(clause) == 0): 
					# if the clause is empty, then all literals evaluted to false, and so the 
					#  solution is unsatisfiable, and we don't write the output...
					write = False
					break

			# Bump up our unique identifier
			configIndex = configIndex + 1

			# Write the output file
			if (write):
				# Compound total number of formulas collected and written so far
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


		# Output the stats (if we actually wrote anything...)
		if (numFormulas > 0):
			# Compute the 2/3 ratio first
			totalRatio = totalRatio + (float(totalTwoClauses) / float(totalThreeClauses))

			# Now display the stats
			print >> sys.stderr, "Total number of formulas: " + str(numFormulas)
			print >> sys.stderr, "Minimum number of 2-clauses: " + str(minTwoClauses)
			print >> sys.stderr, "Maximum number of 2-clauses: " + str(maxTwoClauses)
			print >> sys.stderr, "Average number of 2-clauses: " + str(totalTwoClauses / numFormulas)
			print >> sys.stderr, "Minimum number of 3-clauses: " + str(minThreeClauses)
			print >> sys.stderr, "Maximum number of 3-clauses: " + str(maxThreeClauses)
			print >> sys.stderr, "Average number of 3-clauses: " + str(totalThreeClauses / numFormulas)
			print >> sys.stderr, "Average ratio of 2-to-3 clauses: " + str(totalRatio / numFormulas)

	# Write the resulting CNF file to disk
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
	print >> sys.stderr, "  -sample_size = number of random variable configurations to choose from (enter 2^na to cover them all - DEFAULTS TO 0)"
	print >> sys.stderr, "  -na = number variables assigned"
	print >> sys.stderr, "  -ne = number of edges to add to H"
	print >> sys.stderr, "  -nrr = number of randomly removed vertices"
	print >> sys.stderr, "  -nerr = number of edges randomly removed"
	print >> sys.stderr, "  -nisr = number of maximum independent sets removed"
	print >> sys.stderr, "  -out = output prefix for CNF files"
	print >> sys.stderr, "  -s = random seed"
	print >> sys.stderr, "  -smart = Use the ''smart'' approach for adding edge"
	print >> sys.stderr, "  -saturate = Boolean flag indicating whether or not to saturate the edge set"
	print >> sys.stderr, "  -assign = Perform variable assignment (DEFAULTS TO TRUE)"

def timestampMilli(msg, start, end):
	print >> sys.stderr, msg + str((end - start) * 1000) + "ms"

def main():
	parser = argparse.ArgumentParser(prog='injector')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-sample_size', type=int, default=0)
	parser.add_argument('-na', '--num_assigned', type=int, default=0)
	parser.add_argument('-ne', '--num_edges_to_add', type=int, default=0)
	parser.add_argument('-nrr', '--number_random_removed', type=int, default=0)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int, default=0)
	parser.add_argument('-nerr', type=int, default=0)
	parser.add_argument('-s', '--seed', type=int)
	parser.add_argument('-out', '--out_file', type=str, default="reducedCnf")
	parser.add_argument('-smart',type=bool,default=False)
	parser.add_argument('-saturate',type=bool,default=False)
	parser.add_argument('-assign',type=bool,default=True)
	args = parser.parse_args()

	# Check the command line arguments first...
	if (args.n == None or args.r == None):
		showUsage()
		return -1
	else:
		n = args.n
		r = args.r
		sample_size = args.sample_size
		na = args.num_assigned
		ne = args.num_edges_to_add
		nrr = args.number_random_removed
		nerr = args.nerr
		nisr = args.number_independet_sets_removed
		seed = args.seed
		out = args.out_file
		smart = args.smart
		saturate = args.saturate
		assign = args.assign

		# Seed random...
		random.seed(seed)

		# Create the injector...
		start = time.time()
		inject = injector(n, r, assign, sample_size, na, smart, saturate, ne, nrr, nerr, nisr, out)
		end = time.time()
		timestampMilli("Total time: ", start, end)

if __name__ == "__main__":
	main()

