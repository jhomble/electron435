import compiler as cp
import difflib

def lexer_print_tokens(lexer):
	token = lexer.get_next_token()
	while token.type != 'EOF':
		print (token)
		token = lexer.get_next_token()

def test(textname, resultsname, testname0, keyname0, testname1, keyname1):
	text = open(textname, 'r').read()

	testresults = open(resultsname, 'w')

	testresults.write("TESTING:\n\n")
	makeFacility = True;
	makeImitation = True;

	testresults.write("makeFacility...\n")
	if makeFacility:
		testresults.write("\tLexer...\n")
		facility_lexer = cp.Lexer(text)

		testresults.write("\tParser...\n")
		facility_parser = cp.Parser(facility_lexer)

		testresults.write("\tCompiler...\n")
		facility_compiler = cp.Facility_Domain_Compiler(facility_parser)
		result = facility_compiler.interpret()[0];

		fc_file = open(testname0, 'w')
		fc_file.write("%s" % result)
		testlines = result.strip().splitlines()

		keylines = open(keyname0, 'r').read().strip().splitlines()

		difflinecount = 0;
		# Print diffs of the files if they aren't equal
		for line in difflib.unified_diff(keylines, testlines, fromfile=keyname0, tofile=testname0, lineterm=''):
			if (difflinecount == 0):
				testresults.write("--------- FAILED ---------\nDIFF:\n")
			testresults.write("%s\n" % line)
			difflinecount += 1

		# No diffs, so must be same file
		if (difflinecount == 0):
			testresults.write("--------- PASSED ---------\n\n")

	testresults.write("makeImitation...\n")
	if makeImitation:
		testresults.write("\tLexer...\n")
		imitation_lexer = cp.Lexer(text)

		testresults.write("\tParser...\n")
		imitation_parser = cp.Parser(imitation_lexer)

		testresults.write("\tCompiler...\n")
		imitation_compiler = cp.Imitation_Compiler(imitation_parser)
		result = imitation_compiler.interpret();

		ic_file = open(testname1, 'w')
		ic_file.write("%s" % result)
		testlines = result.strip().splitlines()

		keylines = open(keyname1, 'r').read().strip().splitlines()

		difflinecount = 0;
		# Print diffs of the files if they aren't equal
		for line in difflib.unified_diff(keylines, testlines, fromfile=keyname1, tofile=testname1, lineterm=''):
			if (difflinecount == 0):
				testresults.write("--------- FAILED ---------\nDIFF:\n")
			testresults.write("%s\n" % line)
			difflinecount += 1

		# No diffs, so must be same file
		if (difflinecount == 0):
			testresults.write("--------- PASSED ---------\n\n")	

def main():

	test('causes.txt', 'testfiles/RESULTS.txt', 'testfiles/facility_compiler_test.txt', 'testfiles/facility_compiler_key.txt', 'testfiles/imitation_compiler_test.txt','testfiles/imitation_compiler_key.txt')


if __name__ == '__main__':
   main();

