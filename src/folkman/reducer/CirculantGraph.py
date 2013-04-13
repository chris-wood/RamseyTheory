# File: CirculanhtGrap.py
# Author: Christopher Wood

from networkx import nx

class CirculantGraph:
	''' Class for the ciculant graph.
	'''
	def __init__(self, n, jumps):
		self.graph = nx.Graph()

		# Add the vertices
		for v in range(0, n):
			self.graph.add_node(v)

		# Add the edges
		for x in range(0, n):
			for y in range(0, n):
				

	def removeIndependentSet(self):
		iset = nx.maximal_independent_set(self.graph)
		for v in iset:
			self.graph.remove_node(v)

	def dropNode(self, n):
		if (n < len(self.graph.nodes())):
			self.graph.remove_node(self.graph.nodes()[n])

	def removeNodes(self, n):
		if (n < len(self.graph.nodes())):
			for i in range(n):
				self.graph.remove_node(self.graph.nodes()[0])

	def getGraph(self):
		return self.graph
