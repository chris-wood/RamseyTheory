# File: GNR.py
# Author: Christopher Wood

import sys
from networkx import nx
import random
import pickle

class GNR:
	''' Class for the graph G(n,r) = (Z_n, {(u,v) | u - v = alpha^r mod n}).
	'''
	def __init__(self, n, r, pfile = ""):
		if (pfile == ""):
			self.n = n
			self.r = r
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
		else:
			self.n = n
			self.r = r
			self.graph = pickle.load(open(pfile))

	def removeIndependentSet(self):
		iset = nx.maximal_independent_set(self.graph)
		for v in iset:
			self.graph.remove_node(v)

	def dropNode(self, n):
		if (n < len(self.graph.nodes())):
			self.graph.remove_node(self.graph.nodes()[n])

	def dropEdge(self, e):
		if (e < len(self.graph.edges())):
			u = self.graph.edges()[e][0]
			v = self.graph.edges()[e][1]
			self.graph.remove_edge(u, v)

	# Greedily add as many edges as possible while avoiding K4!
	def saturateAvoidK4(self):
		for x in self.graph.nodes():
			for y in self.graph.nodes():
				if (x != y):
					e = self.makeEdge(x, y)
					print >> sys.stderr, "Trying to add edge: " + str(x) + "-" + str(y)
					if not (self.k4WithEdge(e)):
						self.graph.edges().append(e)

	def addRandomEdgeAvoidK4(self):
		e = self.pickRandomEdge()
		count = 0
		while not (e in self.graph.edges()):
			e = self.pickRandomEdge()
			count = count + 1
			if (count > 100):
				raise Exception("Couldn't find a new edge that didn't already exist after 100 tries...")
		if not (self.k4WithEdge(e)):
			self.graph.edges().append(e)
			return True
		else:
			return False

	def k4WithEdge(self, e):
		# Simply check to see if there exists an edge between all of them...
		u = e[0]
		v = e[1]
		for x1 in self.graph.nodes():
			for x2 in self.graph.nodes():
				edges = []
			 	edges.append(self.makeEdge(u,v))
				edges.append(self.makeEdge(u,x1))
				edges.append(self.makeEdge(u,x2))
				edges.append(self.makeEdge(v,x1))
				edges.append(self.makeEdge(v,x2))
				edges.append(self.makeEdge(x1,x2))
				if self.containsEdges(edges):
					return True
		return False

	def makeEdge(self, u, v):
		if (u <= v):
			return (u,v)
		else:
			return (v,u)

	def containsEdges(self, edges):
		for e in edges:
			if not (self.inEdges(e)):
				return False
		return True # All of them were in the edge set

	def inEdges(self, e):
		if (e[0] < e[1]):
			if e in self.graph.edges():
				return True
		else:
			e2 = (e[1], e[0])
			if e2 in self.graph.edges():
				return True
		return False

	def pickRandomEdge(self):
		u = random.randint(0, self.n)
		v = random.randint(0, self.n)
		count = 0
		while (u == v):
			v = random.randint(0, self.n)
			count = count + 1
			if (count > 100):
				raise Exception("We tried to create a random edge 100 times, but alas, it did not work...")
		if (v < u): # swap, u is always less than v in networkx graphs
			tmp = u
			u = v
			v = tmp
		return (u, v)

	def addEdgeAvoidK4(self, u, v):
		raise TypeError()

	def removeNodes(self, n):
		if (n < len(self.graph.nodes())):
			for i in range(n):
				self.graph.remove_node(self.graph.nodes()[0])

	def getGraph(self):
		return self.graph

	def dump(self, pfile):
		pickle.dump(self.graph, open(pfile, 'w'))
