# File: reduce.py
# Author: Christopher Wood

from networkx import nx

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

	edgeIndex = 0
	for edge in G.edges():

		# TODO: map edges to variables and then generate the CNF formula as needed

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
	G = nx.complete_graph(4)
	numVars, cnf = reduce(G)
	print(makeDimacsCNF(numVars, cnf))

if __name__ == "__main__":
	main()