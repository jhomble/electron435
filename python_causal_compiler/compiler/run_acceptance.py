## Compiler Runner
#
#  This file creates the Lexer and Parser and runs the two
#  compilers.

from Lexer import Lexer
from Parser import Parser
from Facility_Domain_Compiler import Facility_Domain_Compiler
from Imitation_Compiler import Imitation_Compiler
import os
import sys

## Make Facility Domain
#
#  Outputs the first python file that defines CO-PCT tree
def make_facility_domain(interpreter):
	# out_file = os.path.normpath("./python_causal_compiler/compiler/output/acceptance.py")
	out_file = os.path.normpath("./acceptance.py")
	facility_domain_py = open(out_file, "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	print('Opening Facility Domain Template')
	path = os.path.normpath("../../python_causal_compiler/compiler/templates/acceptance_template.txt")
	template = open(path, "r").read()
	# Actually compile input
	print('Running Facility Domain Compiler')
	result, M = interpreter.interpret()

	inserted = template.replace('    # INSERT CAUSES HERE', result)
	inserted = inserted.replace('M = 0 # INSERT M HERE', 'M = '+M)

	facility_domain_py.write(inserted)
	facility_domain_py.close()
	return result

## Make Imitation
#
# Outputs the second python file that uses pyhop to traverse the
# CO-PCT tree
def make_imitation(interpreter):
	out_file = os.path.normpath("./python_causal_compiler/compiler/output/imitation.py")
	imitation_py = open(out_file, "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	print('Opening Imitation Template')
	path = os.path.normpath("./python_causal_compiler/compiler/templates/imitation_template2.txt")
	template = open(path, "r").read()
	# Actually compile input

	# TODO: Use the compiler for imitation, not the same one as facility domain!
	print('Running Imitation Compiler')
	result = interpreter.interpret()

	inserted = template.replace('# INSERT METHODS HERE', result)

	imitation_py.write(inserted)
	imitation_py.close()
	return result

## Run Facility Domain
#
#  Runs the Facility Domain Compiler
def run_facility_domain(text):
	print('Making Lexer')
	lexer = Lexer(text)
	print('Making Parser')	
	parser = Parser(lexer)
	print('Making Facility Domain Compiler')
	facility_compiler = Facility_Domain_Compiler(parser)
	make_facility_domain(facility_compiler)

## Run Imitation
#
#  Runs the Imitation Compiler
def run_imitation(text):
	print('Making Lexer')
	lexer = Lexer(text)
	print('Making Parser')	
	parser = Parser(lexer)
	print('Making Imitation Compiler')
	imitation_compiler = Imitation_Compiler(parser)
	make_imitation(imitation_compiler)

def main():
	print('Opening Causal Input')
	if len(sys.argv) < 3:
		text = sys.argv[1]
	else:
		input_path = os.path.normpath(sys.argv[1])
		text = open(input_path, 'r').read()
	run_facility_domain(text)
	#run_imitation(text)

if __name__ == '__main__':
   main();