# File: reduce.py
# Author: Christopher Wood

from networkx import nx

def reduce(G):
	triangleSet = []

	edgeIndex = 0
	for edge in G.edges():
		edgeIndex = edgeIndex + 1

		# TODO: map edges to variables and then generate the CNF formula as needed

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


def main():
	G = nx.complete_graph(4)
	reduce(G)

if __name__ == "__main__":
	main()