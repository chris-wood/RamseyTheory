''' 
File: GraphGen.py
Author: Lynn Cherny (lynn@ghostweather.com)
Contributor: Christopher Wood
'''

import networkx as nx    # using 1.6, from http://networkx.lanl.gov/ 
from networkx.readwrite import json_graph
from operator import itemgetter
import json 
import sys

class G127:
	def __init__(self, n, r):
		self.graph = nx.Graph()

		# Add the vertices
		for v in range(0, n):
			self.graph.add_node(v)

		# Add the edges
		for x in range(0, n):
			for y in range(0, n):
				for alpha in range(0, n):
					# E(G) = {(x,y) | x-y = alpha^r mod n}
					if (((x - y) % n) == ((alpha ** r) % n)):
						self.graph.add_edge(x, y)

	def getGraph(self):
		return self.graph
	
def save_to_jsonfile(filename, graph):
	''' 
	Save graph object to filename 
	'''
	g = graph
	g_json = json_graph.node_link_data(g) # node-link format to serialize
	f = open(filename, 'w')
	f.write("callback(")
	f.close()
	json.dump(g_json, open(filename,'a'))
	f = open(filename, 'a')
	f.write(")")
	f.close()

def read_json_file(filename, info=True):
	'''
	Use if you already have a json rep of a graph and want to update/modify it
	'''
	graph = json_graph.load(open(filename))
	if info:
		print "Read in file ", filename
		print nx.info(graph)
	return graph
	
def report_node_data(graph, node=""):
	'''
	Will tell you what attributes exist on nodes in the graph.
	Useful for checking your updates.
	'''
	
	g = graph
	if len(node) == 0:
		print "Found these sample attributes on the nodes:"
		print g.nodes(data=True)[0]
	else:
		print "Values for node " + node
		print [d for n,d in g.nodes_iter(data=True) if n==node]
		
def main():

	# Build the output file
	path = '/Users/caw/Projects/RamseyTheory/src/d3render/'

	# TODO: read in cmd line arguments to render the graphs

	# Make G_127...
	g = G127(127,3)
		
	outputjsonfile = 'plot.json'
	save_to_jsonfile(path + outputjsonfile, g.getGraph())
	print("Saved to new file: " + str(path + outputjsonfile))

if __name__ == '__main__':
    main()
