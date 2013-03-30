#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: injector.py
# Author: Christopher Wood

from networkx import nx
from GNR import GNR
from reducer import reducer
import sys
import argparse

# Usage: python injector.py -n -r -na -pl -nrr -nisr 
# -n = n
# -r = r
# -na = number variables assigned
# -pl = variable propagation levels
# -nrr = number of randomly removed vertices
# -nisr = number of independent sets removed

class injector:
	def __init__(self, n, r, na, pl, nrr, nisr):
		self.n = n
		self.r = r
		self.graph = GNR(n, r)
		self.pl = pl
		self.nrr = nrr
		self.nisr = nisr

		# Start stripping...
		self.strip()

	def strip(self):
		raise Exception("asd")

def main():
	parser = argparse.ArgumentParser(prog='injector')
	parser.add_argument('-n', type=int)
	parser.add_argument('-r', type=int)
	parser.add_argument('-na', '--num_assigned', type=int)
	parser.add_argument('-pl', '--propagation_level', type=int)
	parser.add_argument('-nrr', '--number_random_removed', type=int)
	parser.add_argument('-nisr', '--number_independet_sets_removed', type=int)
	args = parser.parse_args()

	# Defaults
	if (args.n == None or args.r == None):
		print("Error: n and r are required.")
	n = args.n
	r = args.r
	na = args.num_assigned
	pl = args.propagation_level
	nrr = args.number_random_removed
	nisr = args.number_independet_sets_removed

	# Create the injector...
	inject = injector(n, r, na, pl, nrr, nisr)

if __name__ == "__main__":
	main()

