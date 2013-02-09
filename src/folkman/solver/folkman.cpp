// Folkman.cpp
// Author: Christopher Wood, caw4567@rit.edu

#include <stdio.h>
#include <vector>

// Storage container for an edge (used in the edge map)
typedef struct 
{
	int x;
	int y;
} edge;

// For convenience...
using namespace std;

vector<bool> results;

void display(int order, int** F)
{
	printf("---\n");
	for (int i = 0; i < order; i++)
	{
		for (int j = 0; j < order; j++)
		{
			printf("%d ", F[i][j]);
		}
		printf("\n");
	}
}

bool isInduced(int order, int n, int edgeCount, int** F, int** colorState, edge* edgeMap, int color)
{
	bool induced = false;

	if (n == 3) // special case for triangles
	{
		//printf("checking for triangle\n");
		for (int edgeIndex = 0; edgeIndex < edgeCount; edgeIndex++) // search over each  edge
		{
			int x = edgeMap[edgeIndex].x;
			int y = edgeMap[edgeIndex].y;
			//printf("examining %d,%d edge\n", x, y);
			if (colorState[x][y] == color)
			{
				for (int v = 0; v < order && (x != v) && (y != v); v++) // check each of the remaining vertices
				{
					//printf("checking possible triangle %d %d (%d)\n", x, y, v);
					//printf("1 %d\n", F[x][v]);
					//printf("2 %d\n", F[y][v]);
					if (F[x][v] == 1 && F[y][v] == 1) // both edges exist
					{
						//display(order, colorState);
						//printf("1 %d\n", colorState[x][v]);
						//printf("2 %d\n", colorState[y][v]);
						if (colorState[x][v] == color && colorState[y][v] == color)
						{
							return true;
						}
					}
				}
			}
		}
	}

	return induced;

/*
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
*/
}

// Walk over all possible colors in the graph F, invoking the k-clique check algorithm for each color
bool walkColors(int order, int color, int** F, int* colors, int** colorState, int edgeCount, edge* edgeMap, int edgeIndex)
{
	// Base case
	if (edgeIndex == edgeCount - 1)
	{
		//printf("new coloring...\n");
		//display(order, colorState);
		int x = edgeMap[edgeIndex].x;
		int y = edgeMap[edgeIndex].y;
		//printf("okay... %d %d\n", x, y);
		for (int c = 0; c < color; c++)
		{
			colorState[x][y] = c;
			colorState[y][x] = c;

			//printf("here we go with induction check\n");
			bool induced = false;
			for (int ci = 0; ci < color; ci++)
			{
				if (isInduced(order, colors[ci], edgeCount, F, colorState, edgeMap, ci))
				{
					//printf("found a triangle in one color!\n");
					induced = true;
				}
			}
			results.push_back(induced);
		}

/*
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
*/

		// walk the color set and check...
		// display the adjacency matrix for debug

	}
	else 
	{
		bool induced = false;
		int x = edgeMap[edgeIndex].x;
		int y = edgeMap[edgeIndex].y;
		//printf("looking at edge %d,%d\n", x, y);
		for (int c = 0; c < color; c++)
		{
			colorState[x][y] = c;
			colorState[y][x] = c;
			if (walkColors(order, color, F, colors, colorState, edgeCount, edgeMap, edgeIndex + 1))
			{
				induced = true;
			}
		}
		return induced;
	}

	// Shouldn't get here...
	return false;

	/*
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
	*/
}

// Decide if F -> (s1, s2, ..., sk)^e
bool folkman(int order, int color, int** F, int* colors)
{
	bool result = true;
	//display(order, F);

	// Allocate space for the color state -  we only use the upper diagnoal of the matrix
	int** colorState = new int*[order];
	for (int i = 0; i < order; i++) 
	{
		colorState[i] = new int[order];
	}

	// Copy over the required portions and set all edge colors to 0
	int edgeCount = 0;
	for (int i = 0; i < order; i++) 
	{
		for (int j = 0; j < order && i >= j; j++) // only look at the upper diagonal
		{
			if (F[i][j] == 1) 
			{
				edgeCount++;
				colorState[i][j] = 0;
				colorState[j][i] = 0;
			}
			else 
			{
				colorState[i][j] = -1; // this edge doesn't exist, so its color is -1
				colorState[j][i] = -1; // Ditto
			}
		}
	}
	printf("edge count = %d\n", edgeCount);
	//display(order, colorState);

	// CAW: THIS IS CORRECT UP TO HERE

	// Allocate and initialize the edge map
	int edgeIndex = 0;
	edge* edgeMap = new edge[edgeCount];
	for (int i = 0; i < order; i++) 
	{
		for (int j = 0; j < order; j++) // only look at the upper diagonal
		{
			//printf("looking at %d,%d\n", i, j);
			if (F[i][j] == 1 && j >= i)
			{
				edge e;
				e.x = i;
				e.y = j;
				//printf("adding edge (%d,%d) to edgeMap\n", e.x, e.y);
				edgeMap[edgeIndex++] = e;
			}
		}
	}

	printf("edge count contents:\n");
	for (int i = 0; i < edgeCount; i++)
	{
		printf("%d,%d\n", edgeMap[i].x, edgeMap[i].y);
	}

	// Now, walk the colors... but to do it sequentially or recursively... that is the question.
	// Python implementation does it recursively
	//printf("starting the color walking routine\n");
	walkColors(order, color, F, colors, colorState, edgeCount, edgeMap, 0);

	// CAW: color permutation appears to be correct

	// 1. generate all possible colorings for F
	// 2. foreach coloring c
	// 2.1 check if K_s in red or K_t in color 0

	return result;
}

#define FSIZE 8

int main(int argc, char** argv)
{
	// K_3 for testing color permutation algorithm
	int** F = new int*[FSIZE];
	for (int i = 0; i < FSIZE; i++)
		F[i] = new int[FSIZE];
	for (int i = 0; i < FSIZE; i++)
	{
		for (int j = 0; j < FSIZE; j++)
		{
			if (i == j) F[i][j] = 0;
			else F[i][j] = 1;
		}
	}

	int* colors = new int[2];
	colors[0] = 3;
	colors[1] = 3;

	//int F[3][3] = {{0, 1, 1}, {1, 0, 1}, {1, 1, 0}};
	//int colors[2] = {0, 1};
	//display(FSIZE, F);
	printf("K_%d -> (3, 3)?\n", FSIZE);
	folkman(FSIZE, 2, F, colors);

	bool foundFalse = false;
	for (int i = 0; i < results.size(); i++)
	{
		if (results[i] == false) 
		{
			foundFalse = true;
			break;
		}
		//printf("result = %d\n", results[i]);
	}
	if (foundFalse)
	{
		printf("No.\n");
	}
	else
	{
		printf("Yes.\n");
	}

	return 0;
}
