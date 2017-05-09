#!/bin/bash

echo "Creating acceptance.py..."
python ../compiler/run_acceptance.py ../compiler/input/acceptance_causes.txt _
echo "Completed!"
echo "Running acceptance.py..."
(echo "n" | python acceptance.py) > acceptance_out.txt
echo "Completed!"
echo "Running baxter_experiments.py..."
(echo "n" | python baxter_experiments.py) > baxter_out.txt
echo "Completed"
echo "Diffing Results..."
diff acceptance_out.txt baxter_out.txt > comparison.txt
echo "Completed"
echo ""
echo "Results available in comparison.txt"