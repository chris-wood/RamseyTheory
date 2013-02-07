# Folkman.py
# Author: Christopher Wood, caw4567@rit.edu

# Don't reinvent the wheel...
from networkx import nx

'''
for each edge (u,v):
  for each vertex w:
     if (v,w) is an edge and (w,u) is an edge:
          return true
return false
'''

def checkPresence(F, n, edgeColor, edgeColorMap, color):
	#print("checking the presence of K_" + str(n) + " for color " + str(color))
	if (n == 3): # Search for triangles with a stupid simple for loop...
		edgeIndex = 0
		show = str(edgeColor) == "[1, 0, 0, 1, 1, 0, 0, 1, 0, 1]" # This edge color set should fail... not return true... figure out what's wrong
		for edgeIndex in range(0, len(edgeColor)):
			edge = F.edges()[edgeIndex]
			if (edgeColor[edgeIndex] == color): # Only look at the specific color
				for vertex in F.nodes():
					#print(F.edges())

					# TODO: why doesn't this work? need to debug on 2/7/13...

					edge1Index = -1
					edge11 = ((edge[0], vertex) in F.edges())# and (edgeColor[(edge[0], vertex)] == color)
					edge12 = ((vertex, edge[0]) in F.edges())# and (edgeColor[(vertex, edge[0])] == color)
					if (edge11):
						edge11 = edgeColor[edgeColorMap[(edge[0], vertex)]] == color
					if (edge12):
						edge12 = edgeColor[edgeColorMap[(vertex, edge[0])]] == color

					edge21 = ((edge[1], vertex) in F.edges())# and (edgeColor[(edge[1], vertex)] == color)
					edge22 = ((vertex, edge[1]) in F.edges())# and (edgeColor[(vertex, edge[1])] == color)
					if (edge21):
						edge21 = edgeColor[edgeColorMap[(edge[1], vertex)]] == color
					if (edge22):
						edge22 = edgeColor[edgeColorMap[(vertex, edge[1])]] == color

					# Check all edge combinations
					if (edge11 or edge12) and (edge21 or edge22):
						if show:
							print("Edge set: " + str(F.edges()))
							print("Colors: " + str(edgeColor))
							print(str(edge) + " - " + str(vertex)) 
						return True
		return False 
	return False

	# TODO: the check should go here..
	# TODO: leverage nauty here...

def walkColors(F, m, n, edgeColor, edgeColorMap, edgeIndex, maxColor, colorSet):
	if (edgeIndex == (len(edgeColor) - 1)):
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			#print("Edges: " + str(F.edges()))
			induced = False

			# We've completed the color assignment... now check to see if there's a K_m in color1/2 or K_n in color1/2
			for color in range(0, maxColor):
				if (checkPresence(F, m, edgeColor, edgeColorMap, color)):
					induced = True
					#print("True for color " + str(color) + " - " + str(edgeColor))
				elif checkPresence(F, n, edgeColor, edgeColorMap, color):
					induced = True
					#print("True for color " + str(color) + " - " + str(edgeColor))

			#if (induced == False):
				#print("False: " + str(edgeColor))

			colorSet.append(induced) # Append the result of this coloring...

	else:
		foundSubgraph = False
		for i in range(0, maxColor):
			edgeColor[edgeIndex] = i
			result = walkColors(F, m, n, edgeColor, edgeColorMap, edgeIndex + 1, maxColor, colorSet)
			if (result):
				foundSubgraph = True
		return foundSubgraph

def folkman(F, m, n):
	''' Decide whether or not F -> (K_m,K_n)
	'''
	# Initialize the edge color sets
	edgeColorMap = {}
	edgeColor = []
	index = 0
	for edge in F.edges():
		edgeColorMap[edge] = index
		edgeColor.append(0) # start with color 0

	# Walk the colors and do the check...
	colorSet = []
	walkColors(F, m, n, edgeColor, edgeColorMap, 0, 2, colorSet) # there's only two colors here...
	for i in colorSet:
		if (i == False):
			return False
	return True

	# brute force algorithm: 
	# - make a copy of F
	# - loop over all possible edge assignments (dictionary from edge -> color)
	# - for each color, check for existince of G and then H in colors

def main():

	# TODO: read in all three params from command line
	# TODO: first must be a graph (adj matrix), second can be graphs or 

	F = nx.complete_graph(5)
	#G = nx.complete_graph(3)
	#H = nx.complete_graph(3)
	print("Checking K_5 -> (3,3)")
	print(folkman(F, 3, 3))

	#F = nx.complete_graph(6)
	#print("Checking K_6 -> (3,3)")
	#folkman(F, 3, 3)

if __name__ == "__main__":
	main()