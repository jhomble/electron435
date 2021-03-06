from compiler import Lexer
from compiler import Parser
from compiler import Facility_Domain_Compiler
from compiler import Imitation_Compiler
import difflib

def lexer_print_tokens(lexer):
	token = lexer.get_next_token()
	while token.type != 'EOF':
		print (token)
		token = lexer.get_next_token()

def test(textname, resultsname, testname0, keyname0, testname1, keyname1):
	text = open(textname, 'r').read()

	testresults = open(resultsname, 'a')

	testresults.write("TESTING %s:\n" % textname)
	makeFacility = True;
	makeImitation = True;

	testresults.write("makeFacility...\n")
	if makeFacility:
		testresults.write("\tLexer...\n")
		facility_lexer = Lexer.Lexer(text)

		testresults.write("\tParser...\n")
		facility_parser = Parser.Parser(facility_lexer)

		testresults.write("\tCompiler...\n")
		facility_compiler = Facility_Domain_Compiler.Facility_Domain_Compiler(facility_parser)
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
		imitation_lexer = Lexer.Lexer(text)

		testresults.write("\tParser...\n")
		imitation_parser = Parser.Parser(imitation_lexer)

		testresults.write("\tCompiler...\n")
		imitation_compiler = Imitation_Compiler.Imitation_Compiler(imitation_parser)
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
	testresults = open('testfiles/RESULTS.txt', 'w')
	test('causes.txt', 'testfiles/RESULTS.txt', 'testfiles/facility_compiler_test.txt', 'testfiles/facility_compiler_key.txt', 'testfiles/imitation_compiler_test.txt','testfiles/imitation_compiler_key.txt')
	test('testfiles/test_conditionals.txt', 'testfiles/RESULTS.txt', 'testfiles/cond_fac_test.txt', 'testfiles/cond_fac_key.txt', 'testfiles/cond_imit_test.txt', 'testfiles/cond_imit_key.txt')


if __name__ == '__main__':
   main();

