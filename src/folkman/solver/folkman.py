# Folkman.py

from networkx import nx

def walkEdges(edgeColor, edgeIndex, maxColor):
	if (edgeIndex == (len(edgeColor) - 1)):
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			print(edgeColor)
	else:
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			walkEdges(edgeColor, edgeIndex + 1, maxColor)

def folkman(F, G, H):
	''' Decide whether or not F -> (G,H)
	'''
	# Initialize the edge color sets
	edgeList = []
	edgeColor = []
	for edge in F.edges():
		edgeList.append(edge)
		edgeColor.append(0) # start with color 0

	walkEdges(edgeColor, 0, 2)

	# Initialize the edge and color index
	#edgeIndex = len(F.edges() - 1)
	#edgeDecrement = 0
	#colorIndex = 0

	# Walk every possible coloring!
	# edgeIndex, edgeDecrement, colorIndex
	#while (edgeIndex > 0):

	# brute force algorithm: 
	# - make a copy of F
	# - loop over all possible edge assignments (dictionary from edge -> color)
	# - for each color, check for existince of G and then H in colors

def main():

	# TODO: read in all three params from command line
	# TODO: first must be a graph (adj matrix), second can be graphs or 

	F = nx.complete_graph(5)
	G = nx.complete_graph(3)
	H = nx.complete_graph(3)
	print("Checking K_6 -> (3,3)")
	folkman(F, G, H)

if __name__ == "__main__":
	main()