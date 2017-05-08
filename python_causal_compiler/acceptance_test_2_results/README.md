# Acceptance Tests Suite 2

These tests are meant to show that functionality from Katz and Reggia's software has been preserved. This is achieved by comparing the results of our generated causes function to the results achieved with the causes function in baxter_experiments.py. The baxter_experiments.py file was slightly modified in order to print out more helpful information but the causes function was not altered.

## Running the Tests

```bash
$ chmod +x run_test_suite_2.sh
$ ./run_test_suite_2.sh
```

## Results

The results should be in comparison.txt once the script is run. They list the test name, followed by the average run time (of 5 trials), followed by the standard deviation (of the same 5 trials). 