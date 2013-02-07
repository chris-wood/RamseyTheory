# Folkman.py
# Author: Christopher Wood, caw4567@rit.edu

# Don't reinvent the wheel...
from networkx import nx

def checkPresence(F, n, edgeColor, edgeColorMap, color):
	''' Check to see if a K_n of color 'color' is in F.

	Note: edgeColor maps edge indices to colors, and edgeColorMap maps edges 
	to edge indices, use as needed.
	'''
	if (n == 3): # Search for triangles with a stupid simple for loop...
		edgeIndex = 0
		for edgeIndex in range(0, len(edgeColor)):
			edge = F.edges()[edgeIndex]
			if (edgeColor[edgeIndex] == color): # Only look at the specific color
				for vertex in F.nodes():
					# Format the edge for linst the index check
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

					# Check to see if we have a triangle of the same color
					if (edge1 in F.edges() and edge2 in F.edges()):
						if (edgeColor[edgeColorMap[edge1]] == color and edgeColor[edgeColorMap[edge2]] == color):
							return True
		return False 
	elif (n == 4):
		print("TODO: 2/7/13")
	else:
		raise Exception("Cases other than n = 3,4 are not yet implemented.")
	return False

def walkColors(F, m, n, edgeColor, edgeColorMap, edgeIndex, maxColor, colorSet):
	''' Walk over all possible colorings for the graph F.

	Note: edgeColor maps edge indices to colors, and edgeColorMap maps edges to edge 
	indices, use as needed. Also, maxColor is the maximum number of colors to check, 
	colorSet is the result of each edge coloring, and m/n are the order of the 
	complete graphs to check.
	'''
	if (edgeIndex == (len(edgeColor) - 1)): # base case - last edge to color
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			induced = False

			# We've completed the color assignment... now check to see if there's a K_m in color1/2 or K_n in color1/2
			for color in range(0, maxColor):
				if (checkPresence(F, m, edgeColor, edgeColorMap, color)):
					induced = True
				elif checkPresence(F, n, edgeColor, edgeColorMap, color):
					induced = True

			# Dump in the result
			colorSet.append(induced)
	else: # keep coloring more edges recursively
		foundSubgraph = False
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			result = walkColors(F, m, n, edgeColor, edgeColorMap, edgeIndex + 1, maxColor, colorSet)
			if (result):
				foundSubgraph = True
		return foundSubgraph

def folkman(F, m, n):
	''' Decide whether or not F -> (K_m,K_n).
	'''
	# Initialize the edge color sets
	edgeColorMap = {}
	edgeColor = []
	index = 0
	for edge in F.edges():
		edgeColorMap[edge] = index
		edgeColor.append(0) # start with color 0
		index = index + 1

	# Walk the colors and do the check...
	colorSet = []
	walkColors(F, m, n, edgeColor, edgeColorMap, 0, 2, colorSet) # there's only two colors here...
	for i in colorSet:
		if (i == False):
			return False
	return True

def main():

	# TODO: read in all three params from command line
	# TODO: first must be a graph (adj matrix), second can be graphs or 

	# The two test cases shown in the presentation...
	F = nx.complete_graph(5)
	print("Checking K_5 -> (3,3)")
	print(folkman(F, 3, 3))

	F = nx.complete_graph(6)
	print("Checking K_6 -> (3,3)")
	print(folkman(F, 3, 3))

if __name__ == "__main__":
	main()