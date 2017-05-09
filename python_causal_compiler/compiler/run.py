# @mainpage Python Causal Compiler!!!
"""
@mainpage Python Causal Compiler
"""

## Compiler Runner
#
#  @filename Facility_Domain_Compiler.py
#  @author Ben Mariano
#  @date 5/9/2017
#
#  @brief This file creates the Lexer and Parser and runs the two
#  compilers.

from Lexer import Lexer
from Parser import Parser
from Facility_Domain_Compiler import Facility_Domain_Compiler
from Imitation_Compiler import Imitation_Compiler
import os
import sys

## Make Facility Domain
#
#  @brief Outputs the first python file that defines CO-PCT tree
#
#  @param interpreter facility domain compiler that will output Python code to be inserted
#  @param log log to keep track of what's going on
#
#  @retval String output of the facility domain compiler
def make_facility_domain(interpreter, log):
	log.write('Opening output file facility_domain.py...\n')
	out_file = os.path.normpath("./python_causal_compiler/compiler/output/facility_domain.py")
	facility_domain_py = open(out_file, "w")
	log.write('Completed opening facility_domain.py!\n\n')

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	log.write('Opening Facility Domain Template...\n')
	path = os.path.normpath("./python_causal_compiler/compiler/templates/facility_domain_template.txt")
	template = open(path, "r").read()
	log.write('Completed opening Facility Domain Template\n\n')

	# Actually compile input
	log.write('Running Facility Domain Compiler...\n')
	result, M = interpreter.interpret()
	log.write('Completed running Facility Domain Compiler\n\n')

	log.write('Adjusting Facility Domain template...\n')
	inserted = template.replace('    # INSERT CAUSES HERE', result)
	inserted = inserted.replace('M = 0 # INSERT M HERE', 'M = '+M)
	log.write('Completed adjusting Facility Domain template!\n\n')

	log.write('Writing to facility_domain.py...\n')
	facility_domain_py.write(inserted)
	facility_domain_py.close()
	log.write('Completed writing to facility_domain.py!\n\n')

	return result

## Make Imitation
#
# @brief Outputs the second python file that uses pyhop to traverse the
# CO-PCT tree
#
#  @param interpreter facility domain compiler that will output Python code to be inserted
#  @param log log to keep track of what's going on
#
#  @retval String output of the imitation compiler
def make_imitation(interpreter, log):
	log.write('Opening output file imitation.py...\n')	
	out_file = os.path.normpath("./python_causal_compiler/compiler/output/imitation.py")
	imitation_py = open(out_file, "w")
	log.write('Completed opening imitation.py!\n\n')	

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	log.write('Opening Imitation Template...\n')	
	path = os.path.normpath("./python_causal_compiler/compiler/templates/imitation_template2.txt")
	template = open(path, "r").read()
	log.write('Completed opening Imitation Template\n\n')

	# Actually compile input

	# TODO: Use the compiler for imitation, not the same one as facility domain!
	log.write('Running Imitation Compiler...\n')
	result = interpreter.interpret()
	log.write('Completed running Imitation Compiler\n\n')

	log.write('Adjusting Imitation template...\n')
	inserted = template.replace('# INSERT METHODS HERE', result)
	log.write('Completed adjusting Imitation template!\n\n')

	log.write('Writing to imitation.py...\n')
	imitation_py.write(inserted)
	imitation_py.close()
	log.write('Completed writing to imitation.py!\n\n')

	return result

## Run Facility Domain
#
#  @brief Runs the Facility Domain Compiler
#
#  @param text string representation of the causal input language text
#  @param log log to keep track of what's going on
#
#  @retval none
def run_facility_domain(text, log):
	log.write('Making Lexer...\n')
	lexer = Lexer(text)
	log.write('Completed making Lexer!\n\n')
	log.write('Making Parser...\n')	
	parser = Parser(lexer)
	log.write('Completed making Parser!\n\n')	
	log.write('Making Facility Domain Compiler...\n')
	facility_compiler = Facility_Domain_Compiler(parser)
	log.write('Completed making Facility Domain Compiler!\n\n')
	make_facility_domain(facility_compiler, log)

## Run Imitation
#
#  @brief Runs the Imitation Compiler
#
#  @param text string representation of the causal input language text
#  @param log log to keep track of what's going on
#
#  @retval none
def run_imitation(text, log):
	log.write('Making Lexer...\n')
	lexer = Lexer(text)
	log.write('Completed making Lexer!\n\n')
	log.write('Making Parser...\n')	
	parser = Parser(lexer)
	log.write('Completed making Parser!\n\n')	
	log.write('Making Imitation Compiler...\n')
	imitation_compiler = Imitation_Compiler(parser)
	log.write('Completed making Imitation Compiler!\n\n')
	make_imitation(imitation_compiler, log)

def main():
	log_file = os.path.normpath("./python_causal_compiler/compiler/logs/compiler/log.txt")
	log = open(log_file, "w")
	error_file = os.path.normpath("./python_causal_compiler/compiler/logs/compiler/error_log.txt")
	error_log = open(error_file, "w")
	completed = 'Successfully completed running run.py!\n'
	log.write('Opening input:\n')	
	if len(sys.argv) < 3:
		log.write('Input is in text form\n\n')
		text = sys.argv[1]
	else:
		log.write('Reading in \'%s\'...\n' % sys.argv[1])
		input_path = os.path.normpath(sys.argv[1])
		try: 
			text = open(input_path, 'r').read()
			log.write('Input was successfully read in!\n\n')
		except Exception as e:
			print('Failed: Check logs at electron435/python_causal_compiler/compiler/logs/compiler')	
			log.write('Failed reading in input file!\n\n')
			error_log.write('Failed reading in input file!\n')
			error_log.write("\tError: %s\n" % e)
			completed = 'Unsuccessfully completed running run.py :(\n'

	try:
		run_facility_domain(text, log)
	except Exception as e:
		print('Failed: Check logs at electron435/python_causal_compiler/compiler/logs/compiler')	
		log.write('Failed in Compilation of Run Facility Domain\n\n')		
		error_log.write('Failed in Compilation of Run Facility Domain\n')
		error_log.write("\tError: %s\n" % e)
		completed = 'Unsuccessfully completed running run.py :(\n'		

	try:
		run_imitation(text, log)
	except Exception as e:
		print('Failed: Check logs at electron435/python_causal_compiler/compiler/logs/compiler')	
		log.write('Failed in Compilation of Run Imitation\n\n')				
		error_log.write('Failed in Compilation of Run Imitation\n')
		error_log.write("\tError: %s\n" % e)
		completed = 'Unsuccessfully completed running run.py :(\n'

	log.write(completed)

	log.close()
	error_log.close()

if __name__ == '__main__':
   main();