#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: reducer.py
# Author: Christopher Wood

from networkx import nx

def makeDimacsCNF(numVars, cnf):
	''' Generate the DIMACS CNF file string for the specified 3-SAT CNF formula.
	'''
	header = "p cnf " + str(numVars) + " " + str(len(cnf))
	clauses = []
	for clause in cnf:
		c = []
		for l in clause:
			c.append(str(l))
		clauses.append(c)
	return header, clauses

class reducer:

	# TODO: need to add (3,4) (4,5) (2,3) (2,4) (2,5) - for generating SAT formulas

	def reduce35(self, G):
		''' Generate the CNF formula for the 3-SAT version of the reduction.
		'''
		triangleSet = []
		k5set = []
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
						cnf.append([edgeMap[edge], edgeMap[edge1], edgeMap[edge2]]) # positive clause
						
						# Find two other vertices that might make the a K_5
						for u in G.nodes():
							for v in G.nodes():
								if (u not in vTuple and v not in vTuple): # two other distinct vertices
									# 1 - u 
									# 2 - v
									# 3 - e0
									# 4 - e1
									# 5 - e2

									# See if we have a K_5 with the other edges...

									edgeList = []

									edge12 = self.makeEdge(u, v)
									edge13 = self.makeEdge(u, vTuple[0])
									edge14 = self.makeEdge(u, vTuple[1])
									edge15 = self.makeEdge(u, vTuple[2])
									edgeList.append(edge12)
									edgeList.append(edge13)
									edgeList.append(edge14)
									edgeList.append(edge15)

									edge21 = self.makeEdge(v, u)
									edge23 = self.makeEdge(u, vTuple[0])
									edge24 = self.makeEdge(u, vTuple[1])
									edge25 = self.makeEdge(u, vTuple[2])
									edgeList.append(edge21)
									edgeList.append(edge23)
									edgeList.append(edge24)
									edgeList.append(edge25)

									edge31 = self.makeEdge(vTuple[0], u)
									edge32 = self.makeEdge(vTuple[0], v)
									edge34 = self.makeEdge(vTuple[0], vTuple[1])
									edge35 = self.makeEdge(vTuple[0], vTuple[2])
									edgeList.append(edge31)
									edgeList.append(edge32)
									edgeList.append(edge34)
									edgeList.append(edge35)

									edge41 = self.makeEdge(vTuple[1], u)
									edge42 = self.makeEdge(vTuple[1], v)
									edge43 = self.makeEdge(vTuple[1], vTuple[0])
									edge45 = self.makeEdge(vTuple[1], vTuple[2])
									edgeList.append(edge41)
									edgeList.append(edge42)
									edgeList.append(edge43)
									edgeList.append(edge45)

									edge51 = self.makeEdge(vTuple[2], u)
									edge52 = self.makeEdge(vTuple[2], v)
									edge53 = self.makeEdge(vTuple[2], vTuple[0])
									edge54 = self.makeEdge(vTuple[2], vTuple[1])
									edgeList.append(edge51)
									edgeList.append(edge52)
									edgeList.append(edge53)
									edgeList.append(edge54)

									k5TupleSet = sorted([u, v, vTuple[0], vTuple[1], vTuple[2]])
									ts = (k5TupleSet[0], k5TupleSet[1], k5TupleSet[2], k5TupleSet[3], k5TupleSet[4])
									if not (ts in k5set):
										k5set.append(ts)
										if (self.containsEdges(edgeList, G)):
											formula = []
											formula.append(edgeMap[edge12] * -1)
											formula.append(edgeMap[edge13] * -1)
											formula.append(edgeMap[edge14] * -1)
											formula.append(edgeMap[edge15] * -1)

											#formula.append(edgeMap[edge21] * -1)
											formula.append(edgeMap[edge23] * -1)
											formula.append(edgeMap[edge24] * -1)
											formula.append(edgeMap[edge25] * -1)

											#formula.append(edgeMap[edge31] * -1)
											#formula.append(edgeMap[edge32] * -1)
											formula.append(edgeMap[edge34] * -1)
											formula.append(edgeMap[edge35] * -1)

											#formula.append(edgeMap[edge41] * -1)
											#formula.append(edgeMap[edge42] * -1)
											#formula.append(edgeMap[edge43] * -1)
											formula.append(edgeMap[edge45] * -1)

											#formula.append(edgeMap[edge51] * -1)
											#formula.append(edgeMap[edge52] * -1)
											#formula.append(edgeMap[edge53] * -1)
											#formula.append(edgeMap[edge54] * -1)

											# Finally, append the formula...
											cnf.append(formula)

						# TODO: search for all other pairs of vertices and see if K_5 is formed, and if so, add negative of their clauses...

						#cnf.append([edgeMap[edge] * -1, edgeMap[edge1] * -1, edgeMap[edge2] * -1]) # negative clause

		# return the CNF formula and number of variables 
		return len(edgeMap), cnf

	def makeEdge(self, u, v):
		if (u <= v):
			return (u,v)
		else:
			return (v,u)

	def containsEdges(self, edges, G):
		for e in edges:
			if not (self.inEdges(e, G)):
				return False
		return True # All of them were inside!

	def inEdges(self, e, G):
		if (e[0] < e[1]):
			if e in G.edges():
				return True
		else:
			e2 = (e[1], e[0])
			if e2 in G.edges():
				return True
		return False

def testK8C5C5():
	K8 = nx.complete_graph(8)
	C1 = nx.cycle_graph(5)
	C2 = nx.cycle_graph(5)

	# Go through the old things here...
	oldNodes = K8.nodes()[:]
	index = len(K8.nodes())
	for v in C1.nodes():
		K8.add_node(v + index)
		for old in oldNodes:
			K8.add_edge(old, v + index)
	for e in C1.edges():
		K8.add_edge(e[0] + index, e[1] + index)
	oldNodes = K8.nodes()[:]
	index = index = len(K8.nodes())
	for v in C2.nodes():
		K8.add_node(v + index)
		for old in oldNodes:
			K8.add_edge(old, v + index)
	for e in C2.edges():
		K8.add_edge(e[0] + index, e[1] + index)

	print(index)
	print(K8.nodes())
	print(K8.edges())
	print(len(K8.edges()))

	# TODO: RUN THE REDUCTION CODE TONIGHT!
	r = reducer()
	numVars, cnf = r.reduce35(K8)
	outFile = open('nenov_arrow_3_5.cnf', 'w')
	header, clauses = makeDimacsCNF(numVars, cnf)
	print(header)
	print(clauses)
	outFile.write(header + "\n")
	for c in clauses:
		for l in c:		
			outFile.write(str(l) + " ")
		outFile.write("0 \n")

def testK8C5():
	K8 = nx.complete_graph(8)
	C1 = nx.cycle_graph(5)

	# Go through the old things here...
	oldNodes = K8.nodes()[:]
	index = len(K8.nodes())
	for v in C1.nodes():
		K8.add_node(v + index)
		for old in oldNodes:
			K8.add_edge(old, v + index)
	for e in C1.edges():
		K8.add_edge(e[0] + index, e[1] + index)

	print(index)
	print(K8.nodes())
	print(K8.edges())
	print(len(K8.edges()))

	# TODO: RUN THE REDUCTION CODE TONIGHT!
	r = reducer()
	numVars, cnf = r.reduce35(K8)
	outFile = open('nenov_arrow_3_5_k5c5.cnf', 'w')
	header, clauses = makeDimacsCNF(numVars, cnf)
	print(header)
	print(clauses)
	outFile.write(header + "\n")
	for c in clauses:
		for l in c:		
			outFile.write(str(l) + " ")
		outFile.write("0 \n")

def main():
	testK8C5()

if __name__ == "__main__":
	main()
