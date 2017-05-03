## Lexer
#
#  Custom language lexer/tokenizer.
from Token import Token

# Token Types
(LPAREN, RPAREN, COMMA, LBRACK, RBRACK, LCURLY, RCURLY, SEMI,
	EQUALS, LESSTHAN, GREATERTHAN, LESSEQUAL, GREATEREQUAL, AND, OR, COLON, ID, INTEGER, CAUSES, DOT, QUOTE, 
	RULES, TYPE, ALL, CONT, IF, EOF) = (
	'LPAREN', 'RPAREN', 'COMMA', 'LBRACK', 'RBRACK', 'LCURLY',
	'RCURLY', 'SEMI', 'EQUALS', 'LESSTHAN','GREATERTHAN', 'LESSEQUAL', 'GREATEREQUAL', 'AND', 'OR', 'COLON', 'ID', 
	'INTEGER', 'CAUSES', 'DOT', 'QUOTE', 'RULES', 'TYPE', 
	'ALL', 'CONT', 'IF', 'EOF'
)

# Automatically tokenizes certain reserved keywords
RESERVED_KEYWORDS = {
	'RULES': Token('RULES', 'RULES'),
	'TYPE':   Token('TYPE', 'TYPE'),
	'ALL':   Token('ALL', 'ALL'),
	'CONT':   Token('CONT', 'CONT'),
	'if': Token('IF', 'IF'),
}

## Custom Lexer
#
#  The Lexer transforms the raw input text from the custom
#  language into a list of tokens
class Lexer(object):
	## Constructor
	def __init__(self, text):
		## @var text
		# Raw input code in custom language
		self.text = text
		## @var pos
		# current index/position in input text
		self.pos = 0
		## @var current_char
		# character at the current index/position
		self.current_char = self.text[self.pos]

	## Lexer Error
	#
	#  Notifies user of use of invalid/unrecognized character
	def error(self):
		raise Exception('Invalid character: {c}'.format(
			c = self.current_char
		))

	## Advance
	#
	#  Changes current position and adjusts current character 
	#  appropriately. Current character is equal to None if the
	#  position is at the end of the input text
	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]

	## Skip Whitespace
	#
	#  Ignores whitespace. Input can have arbitrary spacing.
	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	## Integer
	#
	#  Identifies digits/strings of digits and returns them as integers
	def integer(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()
		return int(result)

	## Peek
	#
	#  Returns the next character without actually moving the current
	#  position. This is needed for certain Lexing decisions.
	def peek(self):
		peek_pos = self.pos + 1
		if peek_pos > len(self.text) - 1:
			return None
		else:
			return self.text[peek_pos]

	## ID
	#
	#  Look in keywords for the given ID and return the corresponding
	#  token
	def _id(self):
		result = ''
		while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '-'):
			result += self.current_char
			self.advance()

		token = RESERVED_KEYWORDS.get(result, Token(ID, result))
		return token

	## Get Next Token
	#
	#  Tokenizes the entire input
	def get_next_token(self):

		while self.current_char is not None:

			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isalpha():
				return self._id()

			if self.current_char.isdigit():
				return Token(INTEGER, self.integer())

			if self.current_char == ':' and self.peek() == '=':
				self.advance()
				self.advance()
				return Token(CAUSES, ':=')

			if self.current_char == ';':
				self.advance()
				return Token(SEMI, ';')									

			if self.current_char == '(':
				self.advance()
				return Token(LPAREN, '(')			

			if self.current_char == ')':
				self.advance()
				return Token(RPAREN, ')')			

			if self.current_char == '[':
				self.advance()
				return Token(LBRACK, '[')			

			if self.current_char == ']':
				self.advance()
				return Token(RBRACK, ']')			

			if self.current_char == ',':
				self.advance()
				return Token(COMMA, ',')			

			if self.current_char == '{':
				self.advance()
				return Token(LCURLY, '{')			

			if self.current_char == '}':
				self.advance()
				return Token(RCURLY, '}')			

			if self.current_char == '=':
				self.advance()
				return Token(EQUALS, '=')

			if self.current_char == '<' and self.peek() != '=':
				self.advance()
				return Token(LESSTHAN,'<')

			if self.current_char == '>' and self.peek() != '=':
				self.advance()
				return Token(GREATERTHAN, '>')

			if self.current_char == '>' and self.peek() == '=':
				self.advance()
				self.advance()
				return Token(GREATEREQUAL,'>=')

			if self.current_char == '<' and self.peek() == '=':
				self.advance()
				self.advance()
				return Token(LESSEQUAL, '<=')

			if self.current_char == '{':
				self.advance()
				return Token(LCURLY, '{')			

			if self.current_char == '&' and self.peek() == '&':
				self.advance()
				self.advance()
				return Token(AND, '&&')			

			if self.current_char == '|' and self.peek() == '|':
				self.advance()
				self.advance()
				return Token(OR, '||')			

			if self.current_char == ':':
				self.advance()
				return Token(COLON, ':')			

			if self.current_char == '.':
				self.advance()
				return Token(DOT, '.')			

			if self.current_char == '\'':
				self.advance()
				return Token(QUOTE, '\'')			

			self.error()

		return Token(EOF, None)
