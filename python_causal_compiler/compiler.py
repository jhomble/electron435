## @package Compiler
#  
#  The following is a Compiler for the custom language specific
#  to the Imitation domain. The custom language syntax is defined
#  here:
#		INSERT LINK HERE TO CAUSAL LANGUAGE SYNTAX NOTES
#
#  The compiler is based on the how-to series entitled 'Let's Build
#  a Simple Interpreter' present at the following link:
#  		https://ruslanspivak.com/lsbasi-part1/

import sys
import functools
import operator

################################################################
#	LEXER
################################################################

# Token Types
(LPAREN, RPAREN, COMMA, LBRACK, RBRACK, LCURLY, RCURLY, SEMI,
	EQUALS, LESSTHAN, GREATERTHAN, LESSEQUAL, GREATEREQUAL, AND, OR, COLON, ID, INTEGER, CAUSES, DOT, QUOTE, 
	RULES, TYPE, ALL, CONT, IF, EOF) = (
	'LPAREN', 'RPAREN', 'COMMA', 'LBRACK', 'RBRACK', 'LCURLY',
	'RCURLY', 'SEMI', 'EQUALS', 'LESSTHAN','GREATERTHAN', 'LESSEQUAL', 'GREATEREQUAL', 'AND', 'OR', 'COLON', 'ID', 
	'INTEGER', 'CAUSES', 'DOT', 'QUOTE', 'RULES', 'TYPE', 
	'ALL', 'CONT', 'IF', 'EOF'
)

## Token Class
#
#  A Token object represents a slightly abstracted piece of syntax
#  from the custom language
class Token(object):
	## Constructor
	def __init__(self, type, value):
		## @var type
		# possible token type: VAR, COMMA, CAUSES, etc.
		self.type = type
		## @var value
		# possible token value: int, float, string, None
		self.value = value

	## To String
	def __str__(self):

		return 'Token({type}, {value})'.format(
			type = self.type,
			value = repr(self.value)
		)

	def __repr__(self):
		return self.__str__()

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
		while self.current_char is not None and self.current_char.isalnum():
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
				return Token(AND, '||')			

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

################################################################
#	Parser
################################################################

## AST
#
#  Abstract Syntax Tree that represents the parse tree of the
#  parsed Tokens
class AST(object):
	pass

## All
#
#  Special ALL keyword. Means all objects in current state with 
#  type arg
class All(AST):
	## Constructor
	def __init__(self, arg):
		## @var arg
		#  The type given as a String argument to keywork ALL.
		self.arg = arg

## Type
#
#  Special TYPE keyword. Means get the type of arg
class Type(AST):
	## Constructor
	def __init__(self, arg):
		## @var arg
		#  The object name as a String whose type is desired
		self.arg = arg

## Digit
#
#  Represents a decimal digit
class Digit(AST):
	## Constructor
	def __init__(self, value):
		## @var value
		#  Contains the single decimal digit as a String
		self.value = value

## Int
#
#  An integer which is represented as a list of digits
class Int(AST):
	## Constructor
	def __init__(self):
		## @var digits
		#  List of digits that comprise the integer (left-to-right)
		self.digits = []

## Float
#
#  Represented as an two integers (separated by a dot syntactically)
class Flt(AST):
	## Constructor
	def __init__(self, left, right):
		## @var left
		#  The integer to the left of the dot
		self.left = left
		## @var right
		#  The integer to the right of the dot
		self.right = right

## Literal
#
#  A string literal, marked in the custom language by quotes
class Literal(AST):
	## Constructor
	def __init__(self, name):
		## @var name
		#  holds the literal value
		self.name = name

## Boolean
#
#  Boolean statement that takes the form:
#     e1 comp e2
#  e1 and e2 are expressions which can be
#  variables, literals, or keyword phrases
#  comp is a comparative operator. Currently
#  only '=' is supported
class Boolean(AST):
	## Constructor
	def __init__(self, e1, op, e2):
		## @var e1
		#  Expression to left of comparitive operator
		self.e1 = e1
		## @var op
		#  Comparative operator (should be '=')
		## @var token
		#  same as op
		self.token = self.op = op
		## @var e2
		#  Expression to right of comparative operator
		self.e2 = e2

## Boolean Expression
#
#  A list of Boolean Statements separated by either &&s or ||s
class BoolExpr(AST):
	## Constructor
	def __init__(self, left, op, right):
		## @var left
		#  Boolean Statement to the left of the operator
		self.left = left
		## @var op
		#  Either && or ||
		## @var token
		#  same as op
		self.token = self.op = op
		## @var left
		#  Boolean Expression to the right of the operator
		self.right = right

## Arguments
#
#  A list of the arguments to an action. For example, the arguments
#  to grasp is a list of one object: [obj]
class Args(AST):
	## Constructor
	def __init__(self):
		## @var children
		#  list of arguments
		self.children = []

## Action
#
#  An action and its arguments
class Act(AST):
	## Constructor
	def __init__(self, var, args):
		## @var var
		#  Name of the action (i.e grasp, release)
		self.var = var
		## @var args
		#  List of actions arguments
		self.args = args

## Actions
#
#  A List of actions
class Acts(AST):
	## Constructor
	def __init__(self):
		## @var children
		#  List of actions
		self.children = []

## Cause
#
#  One causal statement. Act is the intention of the sequence of 
#  actions, acts
class Caus(AST):
	## Constructor
	def __init__(self, act, acts):
		## @var act
		#  The intention
		self.act = act
		## @var acts
		#  The sequence of actions that reduce to act
		self.acts = acts

## Conditional
#
#  Conditional boolean statement that means the causal relation only
#  holds if the boolean statement is true
class Cond(AST):
	## Constructor
	def __init__(self, boolean):
		## @var boolean
		#  boolean guard to conditional
		self.boolean = boolean

## Statement
#
#  A statement is optionally a conditional followed by a causal
#  relation
class Stmt(AST):
	## Constructor
	def __init__(self, cond, caus):
		## @var cond
		#  Conditional to the causal relation. Could be empty
		self.cond = cond
		## @var caus
		#  Causal relation
		self.caus = caus

## Statements
#
#  A List of statements
class Stmts(AST):
	## Constructor
	def __init__(self):
		## @var children
		#  List of statements
		self.children = []

## Variable
#
#  Variables are arguments to actions. They can be referenced in 
#  conditionals or in causal statements, but all derive from 
#  action arguments
class Var(AST):
	## Constructor
	def __init__(self, token):
		## @var token
		#  token representing the variable
		self.token = token
		## @var token
		#  variable value (could be empty)
		self.value = token.value

## No Conditional
#
#  Represents the absence of a conditional
class NoCond(AST):
	pass

## Parser
#
#  Converts a string of tokens into an AST
class Parser(object):
	## Constructor
	def __init__(self, lexer):
		## @var lexer
		#  Lexer that tokenizes input
		self.lexer = lexer
		## @var current_token
		#  the current token being parsed
		self.current_token = self.lexer.get_next_token()

	## Parser Error
	#
	#  Alerts the user of invalid syntax indicated by a 
	#  token that cannot be parsed into an AST object
	def error(self):
		raise Exception('Invalid syntax: {token}'.format(
			token = self.current_token
		))

	## Eat
	#
	#  Advance to next token if there is a next token
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	## Program
	#
	# program -> RULES LCURLY stmts RCURLY
	def program(self):
		self.eat(RULES)
		self.eat(LCURLY)
		node = self.stmts()
		self.eat(RCURLY)
		return node

	## Stmts
	#
	# stmts ->   stmt
	#		   | stmt SEMI stmts
	def stmts(self):
		node = self.stmt()

		root = Stmts()

		root.children.append(node)

		while self.current_token.type == SEMI:
			self.eat(SEMI)
			root.children.append(self.stmt())

		return root

	## Stmt
	#
	# stmt -> cond caus
	def stmt(self):
		node1 = self.cond()
		node2 = self.caus()

		root = Stmt(cond=node1, caus=node2)

		return root

	## Cond
	#
	# cond -> IF LPAREN boolsAnd RPAREN COLON
	#		  | empty		    
	def cond(self):
		if self.current_token.type == IF:
			self.eat(IF)
			self.eat(LPAREN)
			node1 = self.boolsAnd()
			self.eat(RPAREN)
			self.eat(COLON)

			root = Cond(boolean=node1)
		else:
			root = self.empty()

		return root

	## Caus
	#
	# caus -> act CAUSES acts
	def caus(self):
		node1 = self.act()
		self.eat(CAUSES)
		node2 = self.acts()

		root = Caus(act=node1, acts=node2)

		return root

	## Acts
	#
	# acts ->   act COMMA acts
	#	 	  | act
	def acts(self):
		node = self.act()

		root = Acts()

		root.children.append(node)

		while self.current_token.type == COMMA:
			self.eat(COMMA)
			root.children.append(self.act())

		return root

	## Act
	#
	# act -> var LPAREN args RPAREN
	def act(self):
		node1 = self.var()
		self.eat(LPAREN)
		node2 = self.args()
		self.eat(RPAREN)

		root = Act(var=node1, args=node2)

		return root

	## Args
	#
	# args ->   var COMMA args
	#		  | var
	def args(self):
		node = self.var()

		root = Args()

		root.children.append(node)

		while self.current_token.type == COMMA:
			self.eat(COMMA)
			root.children.append(self.var())

		return root

	## BoolsAnd
	#
	# boolsAnd -> boolsOr (AND boolsOr)*
	def boolsAnd(self):
		node = self.boolsOr()

		while self.current_token.type == AND:
			token = self.current_token
			self.eat(AND)

			node = BoolExpr(left=node, op=token, right=self.boolsOr())

		return node

	## BoolsOr
	#
	# boolsOr -> boolean (OR boolean)*
	def boolsOr(self):
		node = self.boolean()

		while self.current_token.type == OR:
			token = self.current_token
			self.eat(OR)

			node = BoolExpr(left=node, op=token, right=self.boolean())

		return node

	## Boolean
	#
	# boolean -> expr EQUALS expr
	def boolean(self):
		node1 = self.expr()
		if self.current_token.type == EQUALS :
			token = self.current_token
			self.eat(EQUALS)
		elif self.current_token.type == LESSTHAN :
			token = self.current_token
			self.eat(LESSTHAN)
		elif self.current_token.type == GREATERTHAN :
			token = self.current_token
			self.eat(GREATERTHAN)
		elif self.current_token.type == GREATEREQUAL :
			token = self.current_token
			self.eat(GREATEREQUAL)
		elif self.current_token.type == LESSEQUAL :
			token = self.current_token
			self.eat(LESSEQUAL)

		node2 = self.expr()

		root = Boolean(e1=node1, op=token, e2=node2)

		return root

	## Expr
	#
	# expr ->   var
	#		  | ALL LPAREN var RPAREN
	#		  | TYPE LPAREN var RPAREN
	#		  | QUOTE var QUOTE
	#		  | LBRACK args RBRACK
	#		  | LPAREN boolsAnd RPAREN
	def expr(self):
		if self.current_token.type == ALL:		
			self.eat(ALL)
			self.eat(LPAREN)
			node = All(arg=self.var())
			self.eat(RPAREN)
		elif self.current_token.type == TYPE:		
			self.eat(TYPE)
			self.eat(LPAREN)
			node = Type(arg=self.var())
			self.eat(RPAREN)
		elif self.current_token.type == QUOTE:					
			self.eat(QUOTE)
			node1 = self.var()
			node = Literal(name=node1)
			self.eat(QUOTE)
		elif self.current_token.type == LBRACK:		
			self.eat(LBRACK)
			node = self.args()
			self.eat(RBRACK)
		elif self.current_token.type == LPAREN:		
			self.eat(LPAREN)
			node = self.boolsAnd
			self.eat(RPAREN)
		else:
			node = self.var()

		return node

	## Var
	#
	# variable ->   ID
	#             | integer
	#             | integer DOT integer    (This is a float)
	#			  | DOT integer            (This is a float)
	def var(self):
		if self.current_token.type == INTEGER:
			node1 = self.integer()
			if self.current_token.type == DOT:
				self.eat(DOT)
				node2 = self.integer()
				node = Flt(left=node1, right=node2)
			else:
				node = node1
		elif self.current_token.type == DOT:
			node1 = Int()
			self.eat(DOT)
			node2 = self.integer()
			node = Float(left=node1, right=node2)
		else:				
			node = Var(self.current_token)
			self.eat(ID)
		
		return node

	## Integer
	#
	# integer ->   INTEGER integer
	#            | INTEGER
	def integer(self):
		node = Digit(self.current_token.value)

		root = Int()

		root.digits.append(node)

		while self.current_token.type == INTEGER:
			root.digits.append(Digit(self.current_token.value))
			self.eat(INTEGER)

		return root

	## Empty
	#
	# empty -> 
	def empty(self):
		return NoCond()

	## Parse Program
	#
	#  Actually runs the parser on the input
	def parse(self):
		node = self.program()

		if self.current_token.type != EOF:
			self.error()

		return node

################################################################
#	Facility_Domain Compiler
################################################################


## Node Visitor
#
#  Visits all nodes of the AST by virtue of the visit_* methods
class NodeVisitor(object):
	## Visit
	#
	# visits the AST node by calling the visit_'node' function
	def visit(self, node):
		method_name = 'visit_'+type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)

	## Visit Error
	#
	# Alerts user if AST node has no defined visit function
	def generic_visit(self, node):
		raise Exception('No visit_{} method'.format(type(node).__name__))

## Facility Domain Compiler
#
#  Compiles the first of the two required python scripts. This 
#  script builds the CO-PCT knowledge base by applying the rules
#  to the input SMILE data.
class Facility_Domain_Compiler(NodeVisitor):

	## Constructor
	def __init__(self, parser):
		## @var parser
		#  Converts input into AST
		self.parser = parser
		## @var M
		#  Length of longest effect sequence (longest list of
		#  actions / right side of a causal relation)
		self.M = 0

	## Visit Literal
	#
	# Returns a tuple of the string 'LITERAL' and the literal
	# value
	#
	# @rtype: (String, String)
	def visit_Literal(self, node):
		return 'LITERAL', str(self.visit(node.name))

	## Visit Boolean
	#
	# Returns a three-tuple of the form e1, comp, e2 where
	# e1 and e2 are tuples representing eithing literals, variables
	# or keyword phrases
	#
	# @rtype: (Tuple, String, Tuple)
	def visit_Boolean(self, node):
		if node.op.type == EQUALS :
			return self.visit(node.e1), "==", self.visit(node.e2)
		elif node.op.type == LESSTHAN :
			return self.visit(node.e1), "<", self.visit(node.e2)
		elif node.op.type == GREATERTHAN :
			return self.visit(node.e1), ">", self.visit(node.e2)
		elif node.op.type == GREATEREQUAL :
			return self.visit(node.e1), ">=", self.visit(node.e2)
		elif node.op.type == LESSEQUAL :
			return self.visit(node.e1), "<=", self.visit(node.e2)

	## Visit Boolean Expression
	#
	# Returns a three tuple of the form b_left, op, b_right
	#
	# @rtype: (Tuple, String, Tuple)
	def visit_BoolExpr(self, node):
		if node.op.type == AND:
			return self.visit(node.left), "&&", self.visit(node.right)
		elif node.op.type == OR:
			return self.visit(node.left) , "||", self.visit(node.right)

	## Visit Arguments
	#
	# Returns a list of strings representing the arguments
	#
	# @rtype: String List
	def visit_Args(self, node):
		args = []
		for child in node.children:
			args.append(self.visit(child))

		return args

	## Visit Action
	#
	# Returns a tuple of the action_name, action_args
	#
	# @rtype: (String, String List)
	def visit_Act(self, node):
		return (self.visit(node.var), self.visit(node.args))

	## Visit Actions
	#
	# Returns a list of strings representing the actions
	#
	# @rtype: (String, String List) List
	def visit_Acts(self, node):
		acts = []
		for child in node.children:
			acts.append(self.visit(child))

		if len(acts) > self.M:
			self.M = len(acts)

		return acts

	## Create Action Argument Index Reference Dictionary
	#
	#  Returns a dictionary where the keys are arguments to the 
	#  actions in a given causal statement and the values are
	#  the associated indices i,j in the 2d arguments array
	#
	# @rtype: {String, (String, String)}
	def create_Action_Arg_Index_Reference_Dict(self, acts):
		arg_index_dict = {}

		for i in range(0, len(acts)):
			for j in range(0, len(acts[i][1])):
				# CONT keyword handled later
				if acts[i][1][j][:4] != 'CONT':
					arg_index_dict[acts[i][1][j]] = str(i),str(j)

		return arg_index_dict 

	## Visit Caus
	#
	# Returns a three tuple of the form if statement, g.add statement,
	# argument indices dictionary.
	#
	# @rtype: (String, String, {String, (String, String)})
	def visit_Caus(self, node):
		# acts = the right-side of the causal statement. Represent
		#		 the actions that cause the 'intention' 
		# act  = the left-side of the causal statement. Represents
		#		 the 'intention' caused by the actions
		acts = self.visit(node.acts)
		act = self.visit(node.act)

		# defines fold-left function
		foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

		# isolates and formats the names of the acts in order to be
		# used in the if statement
		act_names = foldl(operator.add, '', map(lambda x: '\''+x[0]+'\',', acts))

		# if_stmt = initial if statement that differentiates causal
		#			rules
		if_stmt = 'if actions == (' + act_names + '):\n'		

		intention_Args = act[1]

		# arg_indices = creates a dictionary where each key is an 
		#				action from one of the acts and the value
		#				is the i,j indices in the 2d arguments array
		arg_indices = self.create_Action_Arg_Index_Reference_Dict(acts)

		args = ''

		# iterate through all the arguments to the intention
		for a in range(0, len(intention_Args)):
			arg = intention_Args[a] 
			if arg_indices.has_key(arg):
				i,j = arg_indices[arg]
				# Don't add + to last argument string
				if (a == len(intention_Args)-1):
					args += '(arguments['+i+']['+j+'], )' 
				else:
					args += '(arguments['+i+']['+j+'], )+' 
			elif arg[:4] == 'CONT':
					prev_arg = intention_Args[a-1]
					i,j = arg_indices[prev_arg]
					args = args[:len(args)-(18+len(i)+len(j))] + 'arguments['+i+']['+j+':]'
			else:
				raise Exception('Could not find argument: ', arg)

		gadd = 'g.add((states[0],\''+act[0]+'\','+args+'))\n'

		return (if_stmt, gadd, arg_indices)

	## Visit No Conditional
	#
	# Return None when there is no conditional
	def visit_NoCond(self,node):
		return None

	## Visit Conditional
	#
	#  Return the result of evaluating the boolean expression
	def visit_Cond(self, node):
		return self.visit(node.boolean)

	## Compile Boolean Statement
	#
	# Returns a tuple (body, if statement) that represents the 
	# required additions to the output to succesffuly match the 
	# conditional.
	#
	# @rtype: (String, String)
	def compile_bool(self, cond, arg_indices):
		# body     = Additional things added to the body of if_stmt.
		#			 This could include calls to lookup_type or
		#			 defining local variables
		# if_stmt  = Handles conditional relationship rules. For
		#			 example, this if statement would include
		#   		 checking the type of an object		
		body = ''
		if_stmt = ''

		# expr1 = left side of comparison. Could be a variable,
		# 		  literal, or keyword phrase like TYPE(obj)
		# comp  = comparison operator (should be '==')
		# expr2 = right side of comparison. Could be a variable,
		#		  literal, or keyword phrase like ALL(type)
		expr1 = cond[0]
		comp = cond[1]
		expr2 = cond[2]

		if comp == '==':
			if expr1[0] == 'ALL':
				# make the body statement develop a list of all objects of type
				# expr1[1] in the current state (state[0])
				body += 'all_'+expr1[1]+' = [obj_id for (obj_id, obj_type,_,_,_,_)'
				body += ' in states[0] if obj_type == \''+expr1[1]+'\']\n'
				# find argument indices for the left-side of the comparison so
				# that they can be appropriately referenced in the if_stmt
				args = ''
				for a in range(0, len(expr2)):
					arg = expr2[a]
					# Handle the special case of Keyword CONT
					if arg[:4] == 'CONT':
						prev_arg = expr2[a-1]
						i,j = arg_indices[prev_arg]
						args = args[:len(args)-(18+len(i)+len(j))] + 'arguments['+i+']['+j+':]'
					else:
						i,j = arg_indices[arg]
						# don't add + sign if it is the last argument
						if (a == len(expr2) - 1):
							args += '(arguments['+i+']['+j+'], )'
						else:
							args += '(arguments['+i+']['+j+'], )+'
				if_stmt += 'if set(all_'+expr1[1]+') == set('+args+'):\n'
			elif expr1[0] == 'TYPE':
				var_name = str(expr1[1])
				i,j = arg_indices[var_name]
				var_get = 'arguments['+i+']'+'['+j+']'
				body += var_name+'_type = lookup_type('+var_get+', states[0])\n'
				if_stmt += 'if '+var_name+'_type == \''+str(expr2)+'\':\n'
			else:
				# var1 and var2 could be either variables or literals
				var1 = ''
				var2 = ''
				if expr1[0] == 'LITERAL':
					var1 = '\''+str(expr1[1])+'\''
				else:
					i,j = arg_indices[expr1]
					var1 = 'arguments['+i+']['+j+']'

				if expr2[0] == 'LITERAL':
					var2 = '\''+str(expr2[1])+'\''
				else:
					i,j = arg_indices[expr2]
					var2 = 'arguments['+i+']['+j+']'
				if_stmt += 'if '+var1+' == '+var2+':\n'
		else:
			raise Exception('\''+str(comp)+'\' currently not supported')

		return body, if_stmt

	## Visit Statement
	#
	# Returns a String representing a properly compiled full statement,
	# including both a conditional and causal relation. Output is also 
	# appropriately tabbed.
	#
	# @rtype: String
	def visit_Stmt(self, node):
		# if_stmt 	  = initial if statement string that differentiates
		#				which rule is being applied
		# gadd    	  = g.add statement string that adds the result of the 
		#				rule to the final set
		# arg_indices = dictionary containing the i,j indices in the 2d
		#				arguments array for each of the arguments of the
		#				actions
		if_stmt, gadd, arg_indices = self.visit(node.caus)

		# cond = tuple representing the conditions under which the rule
		#		 holds. See visit_BoolExpr for more insight into the 
		#		 formatting here
		cond = self.visit(node.cond)

		# List of accepted comparative operators in Causal Language
		comps = ['==', '<', '>', '<=', '>=']

		# body     = Additional things added to the body of if_stmt.
		#			 This could include calls to lookup_type or
		#			 defining local variables
		# if_stmt2 = Handles conditional relationship rules. For
		#			 example, this if statement would include
		#   		 checking the type of an object
		if_stmt2 = ''
		body = ''

		# Defined to represent a tab in Python (four spaces)
		tab = '    '

		# Only evaluate conditional statements if there are any
		if cond:
			# if cond[1] is one of the comparative operators than we
			# know there is only one boolean statement (no && or ||)
			if cond[1] in comps:
				body, if_stmt2 = self.compile_bool(cond, arg_indices)
				# Only add in tabs for body if there is a body
				if body != '':
					body = 2*tab + body
			else:
				# op  = the previous operand (either && or ||). It 
				#  		starts as 'if' for convenience sake as you'll
				#		see in the code below
				op = 'if'
				# Go through each boolean statement
				for i in range(0, len(cond)):
					# change the operand appropriately to reflect which op it is
					if cond[i] == '&&':
						op = 'and'
					elif cond[i] == '||':
						op = 'or'
					else:
						body2, if_stmt2_2 = self.compile_bool(cond[i], arg_indices)
						# Only add in tabs if the new addition to body 
						# is not empty
						if body2 != '':
							body += 2*tab+body2
						# Replace the ending colon and newline character with a
						# space for the previous if statement. Replace the 'if'
						# from the new if statement with the appropriate operand
						# (either 'and' or 'or'). Doing this allows us to have 
						# the whole conditional on one line, avoiding tabbing issues 
						if_stmt2 = if_stmt2.replace(':\n',' ')+if_stmt2_2.replace('if', op)


		# tabs required before the g.add and second if statements
		# respectively
		gadd_tabs = 3*tab
		if_stmt2_tabs = 2*tab

		# Change the tabbing if there is no conditional
		if if_stmt2 == '':
			if_stmt2_tabs = ''
			gadd_tabs = 2*tab

		# Return appropriately tabbed string of single if statement block
		# from the causes() function in facility_domain.py
		return tab + if_stmt + body + if_stmt2_tabs + if_stmt2 + gadd_tabs + gadd

	## Visit Statements
	#
	# Compile all statements and concatenate results
	#
	# @rtype: String
	def visit_Stmts(self, node):
		result = ''
		for child in node.children:
			result += self.visit(child)

		return result

	## Visit Variable
	#
	# Return a string representing the variable value/name
	# 
	# @rtype: String
	def visit_Var(self, node):
		return str(node.value)

	## Visit Digit
	#
	# Returns a string representing a digit
	#
	# @rtype: String
	def visit_Digit(self, node):
		return str(node.value)

	## Visit Integer
	#
	# Returns a string representing a full integer, which is a 
	# string of concatenated digits
	#
	# @rtype: String
	def visit_Int(self, node):
		result = ''

		for digit in node.digits:
			result += self.visit(digit)

		return result

	## Visit Float
	#
	# Returns a float string which is two integers separated by
	# a dot
	#
	# @rtype: String
	def visit_Flt(self, node):
		return self.visit(node.left) + '.' + self.visit(node.right)

	## Visit ALL
	#
	# Returns a tuple of the form ('All', argument)
	#
	# @rtype: (String, String)
	def visit_All(self, node):
		return ALL, self.visit(node.arg)

	## Visit Type
	#
	# Returns a tuple of the form ('TYPE', argument)
	#
	# @rtype: (String, String)
	def visit_Type(self, node):
		return TYPE, self.visit(node.arg)		

	## Visit NoOp
	#
	# Returns the empty string
	#
	# @rtype: String
	def visit_NoOp(self, node):
		return ''

	## Interpret
	#
	# Actually compile the statement. Returns a tuple of the string 
	# representing the compiled program as well as the value of M
	#
	# @rtype: (String, String)
	def interpret(self):
		tree = self.parser.parse()
		return self.visit(tree), str(self.M)

################################################################
#	Imitation Compiler
################################################################

## Imitation Compiler
#
#  Compiles the second of the two required python scripts. This 
#  script traverses the CO-PCT tree in reverse using PyHop.
class Imitation_Compiler(NodeVisitor):

	## Constructor
	def __init__(self, parser):
		## @var parser
		#  Converts input into AST
		self.parser = parser
		## @var methods_dict
		#  Dictionary of methods where key is method name and
		#  value is a 3-tuple (list of arguments, cond, returns)
		self.methods_dict = {}
		## @var intention
		#  Current intention for access from conditional check
		self.intention = None

	## Visit Literal
	#
	# Returns a tuple of the string 'LITERAL' and the literal
	# value
	#
	# @rtype: (String, String)
	def visit_Literal(self, node):
		return 'LITERAL', str(self.visit(node.name))

	## Visit Boolean
	#
	# Returns a three-tuple of the form e1, comp, e2 where
	# e1 and e2 are tuples representing eithing literals, variables
	# or keyword phrases
	#
	# @rtype: (Tuple, String, Tuple)
	def visit_Boolean(self, node):
		if node.op.type == EQUALS :
			return self.visit(node.e1), "==", self.visit(node.e2)
		elif node.op.type == LESSTHAN :
			return self.visit(node.e1), "<", self.visit(node.e2)
		elif node.op.type == GREATERTHAN :
			return self.visit(node.e1), ">", self.visit(node.e2)
		elif node.op.type == GREATEREQUAL :
			return self.visit(node.e1), ">=", self.visit(node.e2)
		elif node.op.type == LESSEQUAL :
			return self.visit(node.e1), "<=", self.visit(node.e2)

	## Visit Boolean Expression
	#
	# Returns a three tuple of the form b_left, op, b_right
	#
	# @rtype: (Tuple, String, Tuple)
	def visit_BoolExpr(self, node):
		if node.op.type == AND:
			return self.visit(node.left), "&&", self.visit(node.right)
		elif node.op.type == OR:
			return self.visit(node.left) , "||", self.visit(node.right)

	## Visit Arguments
	#
	# Returns a list of strings representing the arguments
	#
	# @rtype: String List
	def visit_Args(self, node):
		args = []
		for child in node.children:
			args.append(self.visit(child))

		return args

	## Visit Action
	#
	# Returns a tuple of the action_name, action_args
	#
	# @rtype: (String, String List)
	def visit_Act(self, node):
		return (self.visit(node.var), self.visit(node.args))

	## Visit Actions
	#
	# Returns a list of strings representing the actions
	#
	# @rtype: (String, String List) List
	def visit_Acts(self, node):
		acts = []
		for child in node.children:
			acts.append(self.visit(child))

		return acts

	## Create Action Argument Index Reference Dictionary
	#
	#  Returns a dictionary where the keys are arguments to the 
	#  actions in a given causal statement and the values are
	#  the associated indices i,j in the 2d arguments array
	#
	# @rtype: {String, (String, String)}
	def create_Action_Arg_Index_Reference_Dict(self, acts):
		arg_index_dict = {}

		for i in range(0, len(acts)):
			for j in range(0, len(acts[i][1])):
				# CONT keyword handled later
				if acts[i][1][j][:4] != 'CONT':
					arg_index_dict[acts[i][1][j]] = str(i),str(j)

		return arg_index_dict 

	## Visit Caus
	#
	# Returns the name of the intention
	#
	# @rtype: String
	def visit_Caus(self, node):
		# acts = the right-side of the causal statement. Represent
		#		 the actions that cause the 'intention' 
		# act  = the left-side of the causal statement. Represents
		#		 the 'intention' caused by the actions
		acts = self.visit(node.acts)
		act = self.visit(node.act)

		# defines fold-left function
		foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

		# isolates and formats the names of the acts in order to be
		# used in the if statement
		act_names = foldl(operator.add, '', map(lambda x: '\''+x[0]+'\',', acts))

		intention_Args = act[1]

		act_name = act[0]

		print('ACT: ' + act_name)

		# return statement
		ret = 'return ['

		# iterate through each action adding it and its 
		# arguments to the return string
		for action in acts:
			ret += '(\''+action[0]+'\','
			for arg in action[1]:
				ret += arg + ','
			ret = ret[:len(ret)-1] + ')'
			ret += ','

		ret = ret[:len(ret)-1] + ']\n'

		print('RET: ' + ret)		

		# Check if method has already been defined
		if self.methods_dict.has_key(act_name):
			args, conds, rets = self.methods_dict[act_name]
			# Check if you have to change parameters (add final *)
			if len(intention_Args) > len(args):
				'TODO: Handle adjustment of args'
				prev_arg = ''				
				for a in range(0, len(intention_Args)):
					arg = intention_Args[a]
					if arg[:4] == 'CONT':
						index = a - int(arg[4:])
						prev_arg = args[index]
						prev_arg = '*' + prev_arg
				adjusted_args = args
				adjusted_args[index] = prev_arg
				self.methods_dict[act_name] = (adjusted_args, conds, rets)

			self.methods_dict[act_name][2].append(ret)
		else:
			self.methods_dict[act_name] = (intention_Args, [], [ret])

		return act_name

	## Visit No Conditional
	#
	# Return None when there is no conditional
	def visit_NoCond(self,node):
		return None

	## Visit Conditional
	#
	#  Return the result of evaluating the boolean expression
	def visit_Cond(self, node):
		result = ''

		boolean = self.visit(node.boolean)

		comps = ['==', '<', '>', '<=', '>=']

		if_stmt = ''
		body = ''

		# holds variable equivalences as determined through
		# conditionals written in custom language
		var_equiv = {}

		# Only evaluate conditional if there are any
		if boolean:
			# if boolean[1] is one of the comparative operators than we
			# know there is only one boolean statement (no && or ||)
			if boolean[1] in comps:
				'TODO: Single boolean statement'
				body, if_stmt, var_equiv = self.compile_bool(boolean, var_equiv)
			else:
				# op  = the previous operand (either && or ||). It 
				#  		starts as 'if' for convenience sake as you'll
				#		see in the code below
				op = 'if'
				# Go through each boolean statement
				for i in range(0, len(boolean)):
					# change the operand appropriately to reflect which op it is
					if boolean[i] == '&&':
						op = 'and'
					elif boolean[i] == '||':
						op = 'or'
					else:
						body2, if_stmt2, var_equiv = self.compile_bool(boolean[i], var_equiv)
						# Only add in tabs if the new addition to body 
						# is not empty
						if body2 != '':
							body += body2
						# Replace the ending colon and newline character with a
						# space for the previous if statement. Replace the 'if'
						# from the new if statement with the appropriate operand
						# (either 'and' or 'or'). Doing this allows us to have 
						# the whole conditional on one line, avoiding tabbing issues
						if if_stmt2 != '': 
							if_stmt = if_stmt.replace(':\n',' ')+if_stmt2.replace('if', op)


		result += body + if_stmt

		return result

	## Compile Boolean Statement
	#
	# Returns a tuple (body, if statement) that represents the 
	# required additions to the output to succesffuly match the 
	# conditional.
	#
	# @rtype: (String, String)
	def compile_bool(self, cond, var_equiv):
		# body     = Additional things added to the body of if_stmt.
		#			 This could include calls to lookup_type or
		#			 defining local variables
		# if_stmt  = Handles conditional relationship rules. For
		#			 example, this if statement would include
		#   		 checking the type of an object		
		body = ''
		if_stmt = ''

		# expr1 = left side of comparison. Could be a variable,
		# 		  literal, or keyword phrase like TYPE(obj)
		# comp  = comparison operator (should be '==')
		# expr2 = right side of comparison. Could be a variable,
		#		  literal, or keyword phrase like ALL(type)
		expr1 = cond[0]
		comp = cond[1]
		expr2 = cond[2]

		intention_Args = self.methods_dict[self.intention][0]

		if comp == '==':
			if expr1[0] == 'ALL':
				'TODO: Compile All keyword'
			elif expr1[0] == 'TYPE':
				var_name = expr1[1]
				if var_name not in intention_Args:
					var_name = expr1[1] + '_TEMP'
				if_stmt += 'if state.objs['+expr1[1]+'][0] == \''
				if_stmt += expr2+'\':\n'
				'TODO: Compile TYPE keyword'
			else:
				'TODO: Compile literal/var comparison'
				# var1 and var2 could be either variables or literals
				var1 = ''
				var2 = ''
				if expr1[0] == 'LITERAL':
					var1 = '\''+str(expr1[1])+'\''
				else:
					i,j = arg_indices[expr1]
					var1 = 'arguments['+i+']['+j+']'

				if expr2[0] == 'LITERAL':
					var2 = '\''+str(expr2[1])+'\''
				else:
					i,j = arg_indices[expr2]
					var2 = 'arguments['+i+']['+j+']'
		else:
			raise Exception('\''+str(comp)+'\' currently not supported')

		return body, if_stmt, var_equiv

	## Visit Statement
	#
	# Evalulates a causal relation and a conditional. Returns None.
	#
	# @rtype: None
	def visit_Stmt(self, node):
		# if_stmt 	  = initial if statement string that differentiates
		#				which rule is being applied
		# gadd    	  = g.add statement string that adds the result of the 
		#				rule to the final set
		# arg_indices = dictionary containing the i,j indices in the 2d
		#				arguments array for each of the arguments of the
		#				actions
		intention = self.visit(node.caus)

		self.intention = intention

		# cond = tuple representing the conditions under which the rule
		#		 holds. See visit_BoolExpr for more insight into the 
		#		 formatting here
		cond = self.visit(node.cond)

		self.methods_dict[intention][1].append(cond)

		return None

	## Visit Statements
	#
	# Compile all statements and concatenate results
	#
	# @rtype: String
	def visit_Stmts(self, node):
		result = ''
		for child in node.children:
			self.visit(child)

		tab = '    '

		print('DICT:')
		for k in self.methods_dict:
			v = self.methods_dict[k]
			print(str(k) + ': ' + str(v))

		for intention in self.methods_dict:
			args = self.methods_dict[intention][0]
			conds = self.methods_dict[intention][1]
			rets = self.methods_dict[intention][2]
			method_dec = 'def '
			method_dec += intention
			method_dec += '(state'
			for arg in args:
				method_dec += ', '+arg
			method_dec += '):\n'
			pyhop_stmt = 'pyhop.declare_methods(\''+intention+'\','
			pyhop_stmt += intention+')\n'
			result += method_dec
			for i in range(0, len(rets)):
				ret = rets[i]
				cond = conds[i]
				if cond:
					result += tab + cond + tab
				result += tab + ret
			result += pyhop_stmt

		return result

	## Visit Variable
	#
	# Return a string representing the variable value/name
	# 
	# @rtype: String
	def visit_Var(self, node):
		return str(node.value)

	## Visit Digit
	#
	# Returns a string representing a digit
	#
	# @rtype: String
	def visit_Digit(self, node):
		return str(node.value)

	## Visit Integer
	#
	# Returns a string representing a full integer, which is a 
	# string of concatenated digits
	#
	# @rtype: String
	def visit_Int(self, node):
		result = ''

		for digit in node.digits:
			result += self.visit(digit)

		return result

	## Visit Float
	#
	# Returns a float string which is two integers separated by
	# a dot
	#
	# @rtype: String
	def visit_Flt(self, node):
		return self.visit(node.left) + '.' + self.visit(node.right)

	## Visit ALL
	#
	# Returns a tuple of the form ('All', argument)
	#
	# @rtype: (String, String)
	def visit_All(self, node):
		return ALL, self.visit(node.arg)

	## Visit Type
	#
	# Returns a tuple of the form ('TYPE', argument)
	#
	# @rtype: (String, String)
	def visit_Type(self, node):
		return TYPE, self.visit(node.arg)		

	## Visit NoOp
	#
	# Returns the empty string
	#
	# @rtype: String
	def visit_NoOp(self, node):
		return ''

	## Interpret
	#
	# Actually compile the statement. Returns a tuple of the string 
	# representing the compiled program as well as the value of M
	#
	# @rtype: (String, String)
	def interpret(self):
		tree = self.parser.parse()
		return self.visit(tree)

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
	facility_domain_py = open("imitation.py", "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	template = open("imitation_template.txt", "r").read()
	# Actually compile input

	# TODO: Use the compiler for imitation, not the same one as facility domain!
	result = interpreter.interpret()

	facility_domain_py.write("%s\n%s" % (template, result))
	facility_domain_py.close()
	return result

def main():
	text = open(sys.argv[1], 'r').read()

	makeFacility = False;
	makeImitation = True;

	if makeFacility:
		facility_lexer = Lexer(text)
		facility_parser = Parser(facility_lexer)
		facility_interpreter = Facility_Domain_Compiler(facility_parser)
		facility_domain_result = make_facility_domain(facility_interpreter)

	if makeImitation:
		imitation_lexer = Lexer(text)
		imitation_parser = Parser(imitation_lexer)
		imitation_interpreter = Imitation_Compiler(imitation_parser)
		imitation_result = make_imitation(imitation_interpreter)

## Index Of
# 
#  Returns the index of obj in the list or -1 if it's not in the list
def indexof(list, obj):
	try:
		index = list.index(obj)
	except:
		return -1;
	else:
		return index

if __name__ == '__main__':
   main();
