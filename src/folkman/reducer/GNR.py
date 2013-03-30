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