# File: reduce.py
# Author: Christopher Wood

from networkx import nx

class GNR:
	''' Class for the graph G(n,r) = (Z_n, {(u,v) | u - v = alpha^r mod n}).
	'''
	def __init__(self, n, r):
		self.graph = nx.Graph()

		# Add the vertices
		for v in range(0, n):
			self.graph.add_node(v)

		# Add the edges
		for x in range(0, n):
			for y in range(0, n):
				if (x != y):
					for alpha in range(0, n):
						# E(G) = {(x,y) | x-y = alpha^r mod n}
						if (((x - y) % n) == ((alpha ** r) % n)):
							self.graph.add_edge(x, y)

	def removeIndependentSet(self):
		iset = nx.maximal_independent_set(self.graph)
		for v in iset:
			self.graph.remove_node(v)

	def removeNodes(self, n):
		if (n < len(self.graph.nodes())):
			for i in range(n):
				self.graph.remove_node(self.graph.nodes()[0])

	def getGraph(self):
		return self.graph

def reduce(G):
	''' Generate the CNF formula for the 3-SAT version of the reduction.
	'''
	triangleSet = []
	edgeMap = {}
	cnf = []

	# Map the edges to integer identifiers
	edgeIndex = 0
	for edge in G.edges():
		edgeIndex = edgeIndex + 1
		edgeMap[edge] = edgeIndex
	print("number of edges = " + str(edgeIndex))

	# Walk the edges, search for triangles, and add clauses to the CNF formula
	edgeIndex = 0
	for edge in G.edges():
		for vertex in G.nodes():
			edge1 = ()
			if (edge[0] < vertex):
				edge1 = (edge[0], vertex)
			else:
				edge1 = (vertex, edge[0])
			edge2 = ()
			if (edge[1] < vertex):
				edge2 = (edge[1], vertex)
			else:
				edge2 = (vertex, edge[1])

			# Check to see if we have a triangle (and add all new triangles to the set)
			if (edge1 in G.edges() and edge2 in G.edges()):
				vSet = sorted([edge[0], edge[1], vertex])
				vTuple = (vSet[0], vSet[1], vSet[2])
				if not (vTuple in triangleSet):
					triangleSet.append(vTuple)
					cnf.append((edgeMap[edge], edgeMap[edge1], edgeMap[edge2])) # positive clause
					cnf.append((edgeMap[edge] * -1, edgeMap[edge1] * -1, edgeMap[edge2] * -1)) # negative clause
	print("number of triangles = " + str(triangleSet))

	# return the CNF formula and number of variables 
	return len(edgeMap), cnf

def makeDimacsCNF(numVars, cnf):
	''' Generate the DIMACS CNF file string for the specified 3-SAT CNF formula.
	'''
	bucket = "p cnf " + str(numVars) + " " + str(len(cnf)) + "\n"
	for clause in cnf:
		v1 = str(clause[0])
		v2 = str(clause[1])
		v3 = str(clause[2])
		bucket = bucket + v1 + " " + v2 + " " + v3 + " 0\n"
	return bucket

def main():
	# G = GNR(127,3)
	# numVars, cnf = reduce(G.graph)
	# outFile = open('out.cnf', 'w')
	# output = makeDimacsCNF(numVars, cnf)
	# outFile.write(output)
	# #print(makeDimacsCNF(numVars, cnf))

	# G.removeIndependentSet()
	# numVars, cnf = reduce(G.graph)
	# outFile = open('out_1.cnf', 'w')
	# output = makeDimacsCNF(numVars, cnf)
	# outFile.write(output)

	# G.removeIndependentSet()
	# numVars, cnf = reduce(G.graph)
	# outFile = open('out_2.cnf', 'w')
	# output = makeDimacsCNF(numVars, cnf)
	# outFile.write(output)

	# G.removeIndependentSet()
	# numVars, cnf = reduce(G.graph)
	# outFile = open('out_3.cnf', 'w')
	# output = makeDimacsCNF(numVars, cnf)
	# outFile.write(output)

	# G = GNR(127,3)
	# n = 47
	# G.removeNodes(47)
	# numVars, cnf = reduce(G.graph)
	# outFile = open('g127_' + str(n) + '.cnf', 'w')
	# output = makeDimacsCNF(numVars, cnf)
	# outFile.write(output)

	n = 47
	for i in range(20):
		G = GNR(127,3)
		numRemove = n - i
		print("Removing " + str(numRemove) + " vertices")
		G.removeNodes(numRemove)
		numVars, cnf = reduce(G.graph)
		outFile = open('g127_' + str(numRemove) + '.cnf', 'w')
		output = makeDimacsCNF(numVars, cnf)
		outFile.write(output)

if __name__ == "__main__":
	main()