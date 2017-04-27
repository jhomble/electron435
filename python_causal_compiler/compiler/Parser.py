## AST and Parser

# Local Imports
import Token
from Lexer import *

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
			print('INTEGER: '+str(self.current_token))
			node1 = self.integer()
			if self.current_token.type == DOT:
				self.eat(DOT)
				print('FLOAT: '+str(self.current_token))				
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
		root = Int()

		# NOT SURE WHY I THOUGHT I NEED THIS
		# IF THERE ARE ERRORS LOOK HERE!
		#node = Digit(self.current_token.value)
		#root.digits.append(node)

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