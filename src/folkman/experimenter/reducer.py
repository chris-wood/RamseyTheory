#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: reduce.py
# Author: Christopher Wood

from GNR import GNR
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
	def reduce(self, G):
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
						cnf.append([edgeMap[edge] * -1, edgeMap[edge1] * -1, edgeMap[edge2] * -1]) # negative clause

		# return the CNF formula and number of variables 
		return len(edgeMap), edgeMap, cnf

	def makeEdge(self, u, v):
		if (u <= v):
			return (u,v)
		else:
			return (v,u)

	def makeHGraphSDP(self, G):
		''' Generate an SDP equivalent output formula for the H_G graph
		'''
		h = nx.Graph()

		# The vertices of H are the edges of G
		for e in G.edges():
			h.add_node(e)

		# Add in the edges of H
		for v1 in G.nodes():
			for v2 in G.nodes():
				for v3 in G.nodes():
					if (v1 != v2 and v1 != v3 and v2 != v3):
						e1 = self.makeEdge(v1, v2)
						e2 = self.makeEdge(v1, v3)
						e3 = self.makeEdge(v2, v3)
						if (e1 in G.edges() and e2 in G.edges() and e3 in G.edges()):
							h.add_edge(e1, e2)
							h.add_edge(e1, e3)
							h.add_edge(e2, e3)
		sdp = str(len(h.nodes())) + " " + str(len(h.edges())) + "\n"
		


def main():
	n = 47 # test...
	for i in range(20):
		G = GNR(127,3)
		numRemove = n - i
		print("Removing " + str(numRemove) + " vertices")
		G.removeNodes(numRemove)
		r = reducer()
		numVars, cnf = r.reduce(G.graph)
		outFile = open('g127_' + str(numRemove) + '.cnf', 'w')

if __name__ == "__main__":
	main()
