## @package pyexample
#  
#  The following is a Compiler for the custom Causal Language specific
#  to the Imitation domain.
#
#  Here is an example of the input language.

import sys
import functools
import operator

################################################################
#	LEXER
################################################################

# Token Types

# Maybe add type, all, Causes, CONT ???
(LPAREN, RPAREN, COMMA, LBRACK, RBRACK, LCURLY, RCURLY, SEMI,
	EQUALS, LESSTHAN, GREATERTHAN, LESSEQUAL, GREATEREQUAL, AND, OR, COLON, ID, INTEGER, CAUSES, DOT, QUOTE, 
	RULES, TYPE, ALL, CONT, IF, EOF) = (
	'LPAREN', 'RPAREN', 'COMMA', 'LBRACK', 'RBRACK', 'LCURLY',
	'RCURLY', 'SEMI', 'EQUALS', 'LESSTHAN','GREATERTHAN', 'LESSEQUAL', 'GREATEREQUAL', 'AND', 'OR', 'COLON', 'ID', 
	'INTEGER', 'CAUSES', 'DOT', 'QUOTE', 'RULES', 'TYPE', 
	'ALL', 'CONT', 'IF', 'EOF'
)

class Token(object):
	def __init__(self, type, value):
		# token type: VAR, COMMA, CAUSES, etc.
		self.type = type
		# token value: int, float, string, None
		self.value = value

	def __str__(self):

		return 'Token({type}, {value})'.format(
			type = self.type,
			value = repr(self.value)
		)

	def __repr__(self):
		return self.__str__()

RESERVED_KEYWORDS = {
	'RULES': Token('RULES', 'RULES'),
	'TYPE':   Token('TYPE', 'TYPE'),
	'ALL':   Token('ALL', 'ALL'),
	'CONT':   Token('CONT', 'CONT'),
	'if': Token('IF', 'IF'),
}

class Lexer(object):
	def __init__(self, text):
		# input code
		self.text = text
		# index in self.text
		self.pos = 0
		self.current_char = self.text[self.pos]

	def error(self):
		raise Exception('Invalid character: {c}'.format(
			c = self.current_char
		))

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def integer(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()
		return int(result)

	def peek(self):
		peek_pos = self.pos + 1
		if peek_pos > len(self.text) - 1:
			return None
		else:
			return self.text[peek_pos]

	def _id(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum():
			result += self.current_char
			self.advance()

		token = RESERVED_KEYWORDS.get(result, Token(ID, result))
		return token

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
class AST(object):
	pass

class All(AST):
	def __init__(self, arg):
		self.arg = arg

class Type(AST):
	def __init__(self, arg):
		self.arg = arg

class Digit(AST):
	def __init__(self, value):
		self.value = value

class Int(AST):
	def __init__(self):
		self.digits = []

class Flt(AST):
	def __init__(self, left, right):
		self.left = left
		self.right = right

class Literal(AST):
	def __init__(self, name):
		self.name = name

class Boolean(AST):
	def __init__(self, e1, op, e2):
		self.e1 = e1
		self.token = self.op = op
		self.e2 = e2

class BoolExpr(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class Args(AST):
	def __init__(self):
		self.children = []

class Act(AST):
	def __init__(self, var, args):
		self.var = var
		self.args = args

class Acts(AST):
	def __init__(self):
		self.children = []

class Caus(AST):
	def __init__(self, act, acts):
		self.act = act
		self.acts = acts

class Cond(AST):
	def __init__(self, boolean):
		self.boolean = boolean

class Stmt(AST):
	def __init__(self, cond, caus):
		self.cond = cond
		self.caus = caus

class Stmts(AST):
	def __init__(self):
		self.children = []

class Var(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class NoCond(AST):
	pass

class Parser(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()

	def error(self):
		raise Exception('Invalid syntax: {token}'.format(
			token = self.current_token
		))

	def eat(self, token_type):
		if self.current_token.type == token_type:
			# DEBUGGING
			print(self.current_token)
			self.current_token = self.lexer.get_next_token()
		else:
			# DEBUGGING
			print("Token Type: ", token_type)			
			self.error()

	def program(self):
		# program -> RULES LCURLY stmts RCURLY
		self.eat(RULES)
		self.eat(LCURLY)
		node = self.stmts()
		self.eat(RCURLY)
		return node

	def stmts(self):
		# stmts ->   stmt
		#		   | stmt SEMI stmts
		node = self.stmt()

		root = Stmts()

		root.children.append(node)

		while self.current_token.type == SEMI:
			self.eat(SEMI)
			root.children.append(self.stmt())

		return root

	def stmt(self):
		# stmt -> cond caus
		node1 = self.cond()
		node2 = self.caus()

		root = Stmt(cond=node1, caus=node2)

		return root

	def cond(self):
		# cond -> IF LPAREN boolsAnd RPAREN COLON
		#		  | empty		    
		print("COND")
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

	def caus(self):
		# caus -> act CAUSES acts
		print("CAUS")
		node1 = self.act()
		self.eat(CAUSES)
		node2 = self.acts()

		root = Caus(act=node1, acts=node2)

		return root

	def acts(self):
		# acts ->   act COMMA acts
		#	 	  | act
		print("ACTS")
		node = self.act()

		root = Acts()

		root.children.append(node)

		while self.current_token.type == COMMA:
			self.eat(COMMA)
			root.children.append(self.act())

		return root

	def act(self):
		# act -> var LPAREN args RPAREN
		print("ACT")
		node1 = self.var()
		self.eat(LPAREN)
		node2 = self.args()
		self.eat(RPAREN)

		root = Act(var=node1, args=node2)

		return root

	def args(self):
		# args ->   var COMMA args
		#		  | var
		node = self.var()

		root = Args()

		root.children.append(node)

		while self.current_token.type == COMMA:
			self.eat(COMMA)
			root.children.append(self.var())

		return root

	def boolsAnd(self):
		# boolsAnd -> boolsOr (AND boolsOr)*
		node = self.boolsOr()

		while self.current_token.type == AND:
			token = self.current_token
			self.eat(AND)

			node = BoolExpr(left=node, op=token, right=self.boolsOr())

		return node

	def boolsOr(self):
		# boolsOr -> boolean (OR boolean)*
		node = self.boolean()

		while self.current_token.type == OR:
			token = self.current_token
			self.eat(OR)

			node = BoolExpr(left=node, op=token, right=self.boolean())

		return node

	def boolean(self):
		# boolean -> expr EQUALS expr
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

	def expr(self):
		# expr ->   var
		#		  | ALL LPAREN var RPAREN
		#		  | TYPE LPAREN var RPAREN
		#		  | QUOTE var QUOTE
		#		  | LBRACK args RBRACK
		#		  | LPAREN boolsAnd RPAREN
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

	def var(self):
		# variable ->   ID
		#             | integer
		#             | integer DOT integer    (This is a float)
		#			  | DOT integer            (This is a float)
		print("VAR")
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

	def integer(self):
		# integer ->   INTEGER integer
		#            | INTEGER

		node = Digit(self.current_token.value)

		root = Int()

		root.digits.append(node)

		while self.current_token.type == INTEGER:
			root.digits.append(Digit(self.current_token.value))
			self.eat(INTEGER)

		return root

	def empty(self):
		return NoCond()

	def parse(self):
		node = self.program()

		if self.current_token.type != EOF:
			self.error()

		return node

################################################################
#	Facility_Domain Compiler
################################################################

class NodeVisitor(object):
	def visit(self, node):
		method_name = 'visit_'+type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)

	def generic_visit(self, node):
		raise Exception('No visit_{} method'.format(type(node).__name__))

class Facility_Domain_Compiler(NodeVisitor):

	def __init__(self, parser):
		self.parser = parser

	def visit_Literal(self, node):
		return 'LITERAL', str(self.visit(node.name))

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

	def visit_BoolExpr(self, node):
		if node.op.type == AND:
			return self.visit(node.left), "&&", self.visit(node.right)
		elif node.op.type == OR:
			return self.visit(node.left) , "||", self.visit(node.right)

	def visit_Args(self, node):
		args = []
		for child in node.children:
			args.append(self.visit(child))

		return args

	def visit_Act(self, node):
		return (self.visit(node.var), self.visit(node.args))

	def visit_Acts(self, node):
		acts = []
		for child in node.children:
			acts.append(self.visit(child))

		return acts

	def create_Action_Arg_Index_Reference_Dict(self, acts):
		arg_index_dict = {}

		for i in range(0, len(acts)):
			for j in range(0, len(acts[i][1])):
				if acts[i][1][j][:4] != 'CONT':
					arg_index_dict[acts[i][1][j]] = str(i),str(j)

		return arg_index_dict 

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

	def visit_NoCond(self,node):
		return None

	def visit_Cond(self, node):
		return self.visit(node.boolean)

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

	def visit_Stmts(self, node):
		result = ''
		for child in node.children:
			result += self.visit(child)

		return result

	def visit_Var(self, node):
		return str(node.value)

	def visit_Digit(self, node):
		return str(node.value)

	def visit_Int(self, node):
		result = ''

		for digit in node.digits:
			result += self.visit(digit)

		return result

	def visit_Flt(self, node):
		return self.visit(node.left) + '.' + self.visit(node.right)

	def visit_All(self, node):
		return ALL, self.visit(node.arg)

	def visit_Type(self, node):
		return TYPE, self.visit(node.arg)		

	def visit_NoOp(self, node):
		return ''

	def interpret(self):
		tree = self.parser.parse()
		return self.visit(tree)

################################################################
#	Imitation Compiler
################################################################

class Imitation_Compiler(NodeVisitor):

	def __init__(self, parser):
		self.parser = parser

	def visit_Literal(self, node):
		return 'LITERAL', str(self.visit(node.name))

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

	def visit_BoolExpr(self, node):
		if node.op.type == AND:
			return self.visit(node.left), "&&", self.visit(node.right)
		elif node.op.type == OR:
			return self.visit(node.left) , "||", self.visit(node.right)

	def visit_Args(self, node):
		args = []
		for child in node.children:
			args.append(self.visit(child))

		return args

	def visit_Act(self, node):
		return (self.visit(node.var), self.visit(node.args))

	def visit_Acts(self, node):
		acts = []
		for child in node.children:
			acts.append(self.visit(child))

		return acts

	def create_Action_Arg_Index_Reference_Dict(acts):
		arg_index_dict = {}

		for i in range(0, len(acts)):
			for j in range(0, len(acts[i])):
				arg_index_dict[acts[i][1][j]] = i,j

		return arg_index_dict 

	def visit_Caus(self, node):
		acts = self.visit(node.acts)
		act = self.visit(node.act)

		foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

		act_names = foldl(operator.add, '', map(lambda x: '\''+x[0]+'\',', acts))

		if_stmt = 'if actions == (' + act_names + '):\n'		

		intention_Args = act[1]

		arg_indices = create_Action_Arg_Index_Reference_Dict(acts)

		# arg_indices = []

		# for arg in intention_Args:
		# 	if arg[:4] != 'CONT':
		# 		for i in range(0, len(acts)):
		# 			j = indexof(acts[i][1], arg)
		# 			if j >= 0:
		# 				arg_indices[arg] = (i,j)
		# 				break
		# 	else:
		# 		if len(arg_indices) == 0:
		# 			raise Exception('Cont used improperly!\n')
		# 		arg_indices[arg] = arg

		# if len(arg_indices) != len(intention_Args):
		# 	raise Exception('Args improperly compiled!')

		# args = ''

		# for a in range(0, len(arg_indices)):
		# 	index = arg_indices[a]
		# 	if index[:4] != 'CONT':
		# 		i = str(index[0])
		# 		j = str(index[1])
		# 		if (a == len(arg_indices)-1):
		# 			args += '(arguments['+i+']['+j+'], )' 
		# 		else:
		# 			args += '(arguments['+i+']['+j+'], )+' 
		# 	else:
		# 		prev_index = arg_indices[a-1]
		# 		i = str(prev_index[0])
		# 		j = str(prev_index[1]+1)
		# 		args += 'arguments['+i+']['+j+':]'

		# args += ')'

		for i in range(0, len(intention_Args)):
			arg = intention_Args[i] 
			if arg_indices.hasKey(arg):
				if len(arg_indices[arg]) == 2:
					i,j = arg_indices[arg]
					if (a == len(arg_indices)-1):
						args += '(arguments['+i+']['+j+'], )' 
					else:
						args += '(arguments['+i+']['+j+'], )+' 
				else:
					'TODO: HANDLE CONT'
		gadd = 'g.add((states[0],\''+act[0]+'\','+args+'))\n'

		print('ARGS: ', args)

		return (if_stmt, gadd)

	def visit_NoCond(self,node):
		return None

	def visit_Cond(self, node):
		return self.visit(node.boolean)

	def compile_bool(self, cond):
		body = ''
		if_stmt = ''

		print('COND: ', str(cond))

		expr1 = cond[0]
		comp = cond[1]
		expr2 = cond[2]

		if comp == '==':
			if expr1[0] == 'ALL':
				print('ALL')

			elif expr1[0] == 'TYPE':
				print('TYPE')
				var_name = str(expr1[1])
				body += var_name+'_type = lookup_type('+var_name+', states[0])\n'
				if_stmt += 'if '+var_name+'_type == \''+str(expr2)+'\':\n'
			else:
				'Var1 = Var2 or Var1 = Literal'
		else:
			raise Exception('\''+str(comp)+'\' currently not supported')

		return body, if_stmt

	def visit_Stmt(self, node):
		if_stmt, gadd = self.visit(node.caus)
		cond = self.visit(node.cond)

		comps = ['==', '<', '>', '<=', '>=']

		if cond:
			if cond[1] in comps:
				print('Single: '+str(cond))
				print(self.compile_bool(cond))
			else:
				print('Multiple: '+str(cond))
				for i in range(0, len(cond)):
					if cond[i] == '&&':
						'TODO: Mess with indenting'
					elif cond[i] == '||':
						'TODO: Mess with indenting'
					else:
						print(self.compile_bool(cond[i]))


		return ''

	def visit_Stmts(self, node):
		result = ''
		for child in node.children:
			result += self.visit(child)

		return result

	def visit_Var(self, node):
		return str(node.value)

	def visit_Digit(self, node):
		return str(node.value)

	def visit_Int(self, node):
		result = ''

		for digit in node.digits:
			result += self.visit(digit)

		return result

	def visit_Flt(self, node):
		return self.visit(node.left) + '.' + self.visit(node.right)

	def visit_All(self, node):
		return ALL, self.visit(node.arg)

	def visit_Type(self, node):
		return TYPE, self.visit(node.arg)		

	def visit_NoOp(self, node):
		return ''

	def interpret(self):
		tree = self.parser.parse()
		return self.visit(tree)

def make_facility_domain(interpreter):
	facility_domain_py = open("facility_domain.py", "w")

	# This block should just be all the text requisite for the file not including cause stuff
	# TODO: Make sure the template is right
	template = open("facility_domain_template.txt", "r").read()
	# Actually compile input
	result = interpreter.interpret()

	inserted = template.replace('\t# INSERT CAUSES HERE', result)

	facility_domain_py.write(inserted)
	facility_domain_py.close()
	return result

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

	lexer = Lexer(text)
	parser = Parser(lexer)
	facility_interpreter = Facility_Domain_Compiler(parser)
	facility_domain_result = make_facility_domain(facility_interpreter)
	#imitation_result = make_imitation(interpreter)

def indexof(list, obj):
	try:
		index = list.index(obj)
	except:
		return -1;
	else:
		return index

if __name__ == '__main__':
   main();
