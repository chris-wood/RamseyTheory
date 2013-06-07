# File: gg.py
# Author: Christopher Wood, caw4567@rit.edu

from networkx import nx
from reducer import reducer
from reducer import makeDimacsCNF
import random
import pickle
import sys

def makeEdge(u, v):
	if (u <= v):
		return (u,v)
	else:
		return (v,u)

def inEdges(g, e):
	if (e[0] < e[1]):
		if e in g.edges():
			return True
	else:
		e2 = (e[1], e[0])
		if e2 in g.edges():
			return True
	return False

def containsEdges(g, edges):
	for e in edges:
		if not (inEdges(g, e)):
			return False
	return True # All of them were in the edge set

def hasK4(g):
	# Simply check to see if there exists an edge between all of them...
	for x1 in g.nodes():
		for x2 in g.nodes():
			for x3 in g.nodes():
				for x4 in g.nodes():
					if x1 != x2 and x1 != x3 and x1 != x4 and x2 != x3 and x2 != x4 and x3 != x4:
						edges = []
					 	edges.append(makeEdge(x1,x2))
						edges.append(makeEdge(x1,x3))
						edges.append(makeEdge(x1,x4))
						edges.append(makeEdge(x2,x3))
						edges.append(makeEdge(x2,x4))
						edges.append(makeEdge(x3,x4))
						if containsEdges(g, edges):
							return True
	return False

def k4WithEdge(g, e):
	# Simply check to see if there exists an edge between all of them...
	u = e[0]
	v = e[1]
	for x1 in g.nodes():
		for x2 in g.nodes():
			edges = []
		 	edges.append(makeEdge(u,v))
			edges.append(makeEdge(u,x1))
			edges.append(makeEdge(u,x2))
			edges.append(makeEdge(v,x1))
			edges.append(makeEdge(v,x2))
			edges.append(makeEdge(x1,x2))
			if containsEdges(g, edges):
				return True
	return False

def saturateAvoidK4(g, vertices):
	for x in vertices:
		for y in vertices:
			if (x != y):
				print >> sys.stderr, "Trying to add edge: " + str(x) + "-" + str(y)
				e = makeEdge(x, y)
				if not (k4WithEdge(g, e)):
					g.edges().append(e)

def buildRandomGraph(nv, npendants, saturate = 1):
	g = nx.Graph()
	for v in range(npendants):
		g.add_node(v)

	nToAdd = nv - npendants
	vertices = []
	for u in range(npendants, nToAdd + npendants):
		g.add_node(u)
		vertices.append(u)
		for v in range(npendants): # pendants get connected to every new vertex that's being added
			g.add_edge(v, u)

	if (saturate == 1):
		saturateAvoidK4(g, vertices)

	if (hasK4(g)):
		raise Exception("No K4 should exist... Check the code.")
	print >> sys.stderr, g.edges()

	return g

def writeCNF(g, fname, numVars, cnf):
	filename = str(fname) + ".pickle"
	pickle.dump(g, open(filename, 'w')) # save the pickled version
	filename = str(fname) + ".out.txt"
	print >> sys.stderr, filename
	f = open(filename, 'wb')
	header, clauses = makeDimacsCNF(numVars, cnf)
	for c in clauses:
		for l in c:
			f.write(str(l) + " ")
		f.write("0 \n")

# Main entry point
if __name__ == "__main__":
	nv = int(sys.argv[1])
	npendants = int(sys.argv[2])
	saturate = int(sys.argv[3])
	iterations = int(sys.argv[4])
	r = reducer()

	# No error checking... use wisely
	for i in range(iterations):
		g = buildRandomGraph(nv, npendants, saturate)
		print >> sys.stderr, "Reducing to 3-SAT"
		numVars, cnf = r.reduce(g)
		print(cnf)
		writeCNF(g, "random_nv" + str(nv) + "_" + str(npendants) + "_" + str(saturate) + "_" + str(i), numVars, cnf)
