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

// Store the results - NO LONGER USED BECAUSE OF MAXIMUM SIZE
vector<bool> results;

// Display the adjacency matrix for the graph F
void display(int order, int** F)
{
	for (int i = 0; i < order; i++)
	{
		for (int j = 0; j < order; j++)
		{
			printf("%d ", F[i][j]);
		}
		printf("\n");
	}
}

// Check to see if K_n is induced by the edges colored in F by 'color'
bool isInduced(int order, int n, int edgeCount, int** F, int** colorState, edge* edgeMap, int color)
{
	bool induced = false;

	if (n == 3) // special case for triangles
	{
		for (int edgeIndex = 0; edgeIndex < edgeCount; edgeIndex++) // search over each  edge
		{
			int x = edgeMap[edgeIndex].x;
			int y = edgeMap[edgeIndex].y;
			if (colorState[x][y] == color)
			{
				for (int v = 0; v < order && (x != v) && (y != v); v++) // check each of the remaining vertices
				{
					if (F[x][v] == 1 && F[y][v] == 1 && colorState[x][v] == color && colorState[y][v] == color) // both edges exist
					{
						return true;
					}
				}
			}
		}
	}
	else if (n == 4)
	{
		for (int edgeIndex = 0; edgeIndex < edgeCount; edgeIndex++) // search over each  edge
		{
			int x = edgeMap[edgeIndex].x;
			int y = edgeMap[edgeIndex].y;
			if (colorState[x][y] == color)
			{
				for (int v = 0; v < order && (x != v) && (y != v); v++) // check each of the remaining vertices
				{
					if (F[x][v] == 1 && F[y][v] == 1 && colorState[x][v] == color && colorState[y][v] == color) // both edges exist
					{
						// TODO: continue check for fourth vertex thats in the set...
						for (int v2 = 0; v2 < order && (v2 != v) && (v2 != x) && (v2 != y); v2++)
						{
							if (F[v2][x] == 1 && F[v2][y] && F[v2][v] && 
								colorState[v2][x] == color && colorState[v2][y] == color && colorState[v2][v] == color)
							{
								return true;
							}
						}
					}
				}
			}
		}
	}
	else 
	{
		printf("Error: only n = 3,4 clique sizes are supported.\n");
	}

	return induced;
}

// Walk over all possible colors in the graph F, invoking the k-clique check algorithm for each color
bool walkColors(int order, int color, int** F, int* colors, int** colorState, int edgeCount, edge* edgeMap, int edgeIndex)
{
	// Base case
	if (edgeIndex == edgeCount - 1)
	{
		int x = edgeMap[edgeIndex].x;
		int y = edgeMap[edgeIndex].y;
		for (int c = 0; c < color; c++)
		{
			colorState[x][y] = c;
			colorState[y][x] = c;
			bool induced = false;
			for (int ci = 0; ci < color; ci++)
			{
				if (isInduced(order, colors[ci], edgeCount, F, colorState, edgeMap, ci))
				{
					induced = true;
				}
			} 
			// TODO: Append results to the vector 
			if (induced == false)
			{
				return induced;
			}
		}
		return true;
	}
	else 
	{
		bool induced = false;
		int x = edgeMap[edgeIndex].x;
		int y = edgeMap[edgeIndex].y;
		for (int c = 0; c < color; c++)
		{
			colorState[x][y] = c;
			colorState[y][x] = c;
			if (walkColors(order, color, F, colors, colorState, edgeCount, edgeMap, edgeIndex + 1))
			{
				induced = true;
			} 
			else {
				return false;
			}
		}
		return induced;
	}
}

// Decide if F -> (s1, s2, ..., sk)^e
bool folkman(int order, int color, int** F, int* colors)
{
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

	// Allocate and initialize the edge map
	int edgeIndex = 0;
	edge* edgeMap = new edge[edgeCount];
	for (int i = 0; i < order; i++) 
	{
		for (int j = 0; j < order; j++) // only look at the upper diagonal
		{
			if (F[i][j] == 1 && j >= i)
			{
				edge e;
				e.x = i;
				e.y = j;
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
	bool result = walkColors(order, color, F, colors, colorState, edgeCount, edgeMap, 0);

	/*bool result = true;
	for (int i = 0; i < results.size(); i++)
	{
		if (results[i] == false) 
		{
			result = false;
			break;
		}
	}*/

	return result;
}

// Define the order of the first graph
#define FSIZE 9

int main(int argc, char** argv)
{
	// K_FSIZE for testing color permutation algorithm
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
	colors[0] = 4;
	colors[1] = 3;

	// Run the checks now...
	printf("K_%d -> (%d, %d)?\n", FSIZE, colors[0], colors[1]);
	bool result = folkman(FSIZE, 2, F, colors);
	if (result) printf("Yes.\n");
	else printf("No.\n");

	return 0;
}
