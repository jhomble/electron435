import compiler as cp

def lexer_print_tokens(lexer):
	token = lexer.get_next_token()
	while token.type != 'EOF':
		print (token)
		token = lexer.get_next_token()

def main():
	text = open('causes.txt', 'r').read()

	print("TESTING:")
	makeFacility = True;
	makeImitation = True;

	print("makeFacility...")
	if makeFacility:
		print("\tLexer...")
		facility_lexer = cp.Lexer(text)
		print("\tParser...")
		facility_parser = cp.Parser(facility_lexer)
		print("\tCompiler...")
		facility_compiler = cp.Facility_Domain_Compiler(facility_parser)

	print("makeImitation...")
	if makeImitation:
		print("\tLexer...")
		imitation_lexer = cp.Lexer(text)
		print("\tParser...")
		imitation_parser = cp.Parser(imitation_lexer)
		print("\tCompiler...")
		imitation_compiler = cp.Imitation_Compiler(imitation_parser)

if __name__ == '__main__':
   main();

