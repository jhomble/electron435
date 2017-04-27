from Lexer import Lexer
from Parser import Parser
from Facility_Domain_Compiler import Facility_Domain_Compiler
from Imitation_Compiler import Imitation_Compiler

## Make Facility Domain
#
#  Outputs the first python file that defines CO-PCT tree
def make_facility_domain(interpreter):
	facility_domain_py = open("facility_domain.py", "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	template = open("facility_domain_template.txt", "r").read()
	# Actually compile input
	result, M = interpreter.interpret()

	inserted = template.replace('\t# INSERT CAUSES HERE', result)
	inserted = inserted.replace('M = 0 # INSERT M HERE', 'M = '+M)

	facility_domain_py.write(inserted)
	facility_domain_py.close()
	return result

## Make Imitation
#
# Outputs the second python file that uses pyhop to traverse the
# CO-PCT tree
def make_imitation(interpreter):
	imitation_py = open("imitation.py", "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	template = open("imitation_template.txt", "r").read()
	# Actually compile input

	# TODO: Use the compiler for imitation, not the same one as facility domain!
	result = interpreter.interpret()

	inserted = template.replace('# INSERT METHODS HERE', result)

	imitation_py.write(inserted)
	imitation_py.close()
	return result

def main():
	print('TESTING')
	text = open('causes.txt', 'r').read()

	print('TESTING LEXER')
	lexer = Lexer(text)
	print('TESTING Parser')	
	parser = Parser(lexer)
	print('TESTING FACILITY_DOMAIN_COMPILER')
	facility_compiler = Facility_Domain_Compiler(parser)
	make_facility_domain(facility_compiler)

	print('TESTING LEXER')
	lexer = Lexer(text)
	print('TESTING Parser')	
	parser = Parser(lexer)
	print('TESTING IMITATION_COMPILER')
	imitation_compiler = Imitation_Compiler(parser)
	make_imitation(imitation_compiler)



if __name__ == '__main__':
   main();