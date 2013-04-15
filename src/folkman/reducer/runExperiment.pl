#!/bin/bash

# Run the injector program to generate the sample list
# NOTE: arguments are TIGHTLY coupled to the program's input - be careful - check injector.py for usage
#python injector.py -n $1 -r $2 -sample $3 -na $4 -ne $5 -nrr $6 -nerr $7 -nisr $8 -out $9 2> out 1> fileList

echo "Running minisat on the generated formulas..."

# Loop through each file in the out list
COUNTER=0;
while read p; do
	# Display the current file...
	echo $p

	# Run minisat for AT MOST five hours before killing it...
	( cmdpid=$BASHPID; (sleep 18000; kill $cmdpid) & minisat $p > experiment_out_$COUNTER )

	# Bump up the counter
	let COUNTER=COUNTER+1 
done < fileList
