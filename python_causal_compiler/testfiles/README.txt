Compiler Unit Testing

-- Adding a test to test.py --

1. Navigate to the main() function of test.py

2. Insert a new call to test() as follows:
	test(textname, resultsname, testname0, keyname0, testname1, keyname1)
		textname: 		Path of the causal knowledge text function.
		resultsname:	Path of the file you would like to add the results to.
			If you would like to use a new file, be sure to Open() the file
			first as the test() function appends to the existing file passed in.
		testname0:		Path of the file your test's compiled output for the
			"facility" file.
		keyname0:		Path of the file that contains the key to compare
			against for testname0.
		testname1:		Path of the file your test's compiled output for the
			"imitation" file.
		keyname1:		Path of the file that contains the key to compare
			against for testname1.
	See the main() function for examples.

3. Run test.py and see your various output files. Your file passed in as
	resultsname will output a diff of your actual output versus the key output
	you provided.