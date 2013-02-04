'''
File: GraphUtil.py
Author: Christopher Wood
Version: 2/4/13
'''

import networkx as nx    # using 1.6, from http://networkx.lanl.gov/ 
from networkx.readwrite import json_graph
from operator import itemgetter
import json 
import sys

def calculate_degree(graph):
	''' Calculate the maximum and minimum degree of the graph.
	'''
	g = graph
	deg = nx.degree(g)
	nx.set_node_attributes(g,'degree',deg)
	return g, deg

def calculate_indegree(graph):
	'''Will only work on DiGraph (directed graph)
	Saves the indegree as attribute on the node, and returns graph, dict of indegree
	'''
	g = graph
	indeg = g.in_degree()
	nx.set_node_attributes(g, 'indegree', indeg)
	return g, indeg
	
def calculate_outdegree(graph):
	'''Will only work on DiGraph (directed graph)
	Saves the outdegree as attribute on the node, and returns graph, dict of outdegree
	'''
	g = graph
	outdeg = g.out_degree()
	nx.set_node_attributes(g, 'outdegree', outdeg)
	return g, outdeg

def calculate_betweenness(graph):
	''' Calculate betweenness centrality of a node, sets value on node as attribute; returns graph, and dict of the betweenness centrality values
	'''
	g = graph
	bc=nx.betweenness_centrality(g)
	nx.set_node_attributes(g,'betweenness',bc)
	return g, bc
	
def calculate_eigenvector_centrality(graph):  
	''' Calculate eigenvector centrality of a node, sets value on node as attribute; returns graph, and dict of the eigenvector centrality values.
	Also has commented out code to sort by ec value
	'''
	g = graph
	ec = nx.eigenvector_centrality(g)
	nx.set_node_attributes(g,'eigen_cent',ec)
	#ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
	return g, ec

def calculate_degree_centrality(graph):
	''' Calculate degree centrality of a node, sets value on node as attribute; returns graph, and dict of the degree centrality values.
	Also has code to print the top 10 nodes by degree centrality to console
	'''
	g = graph
	dc = nx.degree_centrality(g)
	nx.set_node_attributes(g,'degree_cent',dc)
	degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
	for key,value in degcent_sorted[0:10]:
		print "Highest degree Centrality:", key, value
	return graph, dc

def find_cliques(graph):
	''' Calculate cliques and return as sorted list.  Print sizes of cliques found.
	'''
	g = graph
	cl = nx.find_cliques(g)
	cl = sorted(list( cl ), key=len, reverse=True)
	print "Number of cliques:", len(cl)
	cl_sizes = [len(c) for c in cl]
	print "Size of cliques:", cl_sizes
	return cl