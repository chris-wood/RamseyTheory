# File: btsizer.py
# Author: Christopher A. Wood
# Description: Estimate the size of a backtracking search space tree using the Stinson/Keuhler method

N = 0
m = 0
C = []

def probe(l):
	global N
	global m
	global C

	# Compute Cl for the node [x0,..,xl-1]
	c = 0 # c = |Cl|, size of the set

	if (c != 0):
		m = m * c
		N = N + m
		# xl = random element of Cl
		# Probe(l + 1)

	print("inside probe")

def main():
	global N
	global m

	N = 1
	m = 0
	probe(0)

if __name__ == "__main__":
	main()