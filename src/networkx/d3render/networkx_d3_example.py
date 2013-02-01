#!/usr/bin/env python
# encoding: utf-8
"""
File: parseGraphToRender.py
"""

# Load the right version of the library
import sys
sys.path.append("/Users/caw/Libraries/networkx")

# Load the D3.js support
import networkx as nx
from networkx.readwrite import d3_js

def main():
	plot = nx.read_graphml('test.graphml')
	label_dict = dict(map(lambda i : (mikedewar.nodes()[i], plot.nodes(data=True)[i][1]['Label']), xrange(plot.number_of_nodes())))
	plot_d3 = nx.relabel_nodes(plot, label_dict)	

	# Export 
	d3_js.export_d3_js(plot_d3, files_dir="web", graphname="plot", group="REC", node_labels=False)

if __name__ == '__main__':
	main()

	

