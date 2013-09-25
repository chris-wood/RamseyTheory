# File: GNR.py
# Author: Christopher Wood

import sys
from networkx import nx
from networkx.algorithms import isomorphism
import random
import pickle
from itertools import combinations


def count_edges_between_sets(B, R):
	count = 0
	for ei in B:
		for ej in R:
			if ei[0] == ej[0]:
				count = count + 1
			if ei[0] == ej[1]:
				count = count + 1
			if ei[1] == ej[0]:
				count == count + 1
			if ei[1] == ej[1]:
				count = count + 1
	return count

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

	

#	def is_edge_set_adjacent(self, edges):
#		''' TODO: this only works for triangles... I need to change that.
#		'''
#		for i in range(len(edges)):
#			v1 = edges[i][0]
#			v2 = edges[i][1]
#			v1Match = False
#			v2Match = False
#			for j in range(len(edges)):
#				if (i != j):
#					if v1 == edges[j][0] or v1 == edges[j][1]:
#						v1Match = True
#					if v2 == edges[j][0] or v2 == edges[j][1]:
#						v2Match = True
#				if (v1Match and v2Match):
#					break
#			if (v1Match == False or v2Match == False):
#				return False
#		return True

	def random_edge_split(self, n):
		''' Randomly split the edges of G into n bags.
		'''
		bags = {}
		for e in self.graph.edges():
			b = random.randint(0, n - 1)
			if not (b in bags):
				bags[b] = []
			bags[b].append(e)
		return bags


	def find_rb_neighbors(self, v, bags):
		B = []
		R = []
		for e in self.graph.edges():
			if v == e[0] or v == e[1]:
				if e in bags[0]:
					B.append(e)
				elif e in bags[1]:
					R.append(e)
		return B, R

	def find_candidate_rb_split(self, nv):
		raise Exception("TODO: pick random vertex such that n(v) >= 157")

	def iterative_edge_split_avoid_kn(self, b, n):
		''' Randomly split the edges of G into n bags.
		'''
		bags = {}
		Kn = nx.complete_graph(n)
		for e in self.graph.edges():
			colors = 0
			while colors != b:
				color = colors
				if not (color in bags):
					bags[color] = []

				# Check to see if adding e to the 'color' bag yields a monochromatic Kn
				edges = []
				G = nx.Graph()
				#for ee in bags[color]:
				#	try:
				#		G.add_node(ee[0])
				#	except:
				#		pass
				#	try:
				#		G.add_node(ee[1])
				#	except:
				#		pass
				# Add the edges now...
				G.add_edges_from(bags[color])
				#try:
				#	G.add_node(e[0])
				#except:
				#	pass
				#try:
				#	G.add_node(e[1])
				#except:
				#	pass
				G.add_edges_from([e])

				# Set up and check for subgraph isomorphism
				# If it contains a Kn, then don't color the edge with that color, try another one...
				GM = isomorphism.GraphMatcher(G, Kn)
				if GM.subgraph_is_isomorphic() == False:
					bags[color].append(e)
					break
				else:
					colors = colors + 1
			if colors == b:
				#raise Exception("Could not find a color to add edge: " + str(e))
				return None
		return bags

	def edge_bags_contains_kn(self, bags, n):
		''' Check to see if bags (map : int => []) contains monochromatic kn in any bag.
		'''
		Kn = nx.complete_graph(n)
		for b in bags:
			#indices = list(combinations(range(len(bags[b])),n))
			#print >> sys.stderr, "C(n,k) = " + str(len(indices))
			#for ind in indices:
			edges = []
			G = nx.Graph()
			#for i in ind:
			#try:
			#	G.add_node(bags[b][i][0])
			#except:
			#	pass
			#try:
			#	G.add_node(bags[b][i][1])
			#except:
			#	pass
			#edges.append(bags[b][i])
				
			# Build induced subgraph from this set of edges and then check to see
			# if Kn is an induced subgraph in G
			G.add_edges_from(bags[b])
			GM = isomorphism.GraphMatcher(G, Kn)
			if GM.subgraph_is_isomorphic():
				return True

			#if self.is_edge_set_adjacent(edges):
			#	return True
		return False # out of all C(n,k) choices, none yielded monochromatic Kn in the same bag
	
#	def iterative_edge_split_avoid_kn(self, b, n):
#		print >> sys.stderr, "Still trying to find a proper coloring..."
#		bags = self.iterative_edge_split_avoid_kn(b, n)
#		print >> sys.stderr, "Found a bag, checking for Kn containment with n = " + str(n)
#		if self.edge_bags_contains_kn(bags, n):
#			raise Exception("This should not happen!")
#		return bags

	def random_edge_split_avoid_kn(self, b, n):
		print >> sys.stderr, "Still trying to find a proper coloring..."
		bags = self.random_edge_split(b)
		print >> sys.stderr, "Found a bag, checking for Kn containment with n = " + str(n)
		count = 0
		while (self.edge_bags_contains_kn(bags, n)):
			count = count + 1
			bags = self.random_edge_split(b)
			if (count % 500 == 0):
				print >> sys.stderr, "Still trying to find a proper coloring..."
		return bags

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
