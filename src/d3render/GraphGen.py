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
	
def save_to_jsonfile(filename, graph):
	''' 
	Save graph object to filename 
	'''
	g = graph
	g_json = json_graph.node_link_data(g) # node-link format to serialize
	json.dump(g_json, open(filename,'w'))

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

	path = '/Users/caw/Projects/RamseyTheory/src/d3render/'

	# Make G_127...
	g = nx.Graph()
	for v in range(0, 127):
		g.add_node(v)
	for x in range(0, 127):
		for y in range(0, 127):
			g.add_edge(x, y)
	
	outputjsonfile = 'full_1644nodes_test.json'
	save_to_jsonfile( path+outputjsonfile, g)
	print "Saved to new file: ", path+outputjsonfile

if __name__ == '__main__':
    main()
