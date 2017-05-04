## Facility Domain Compiler

# Library Imports
import operator
import functools

# Local Imports
import Token
from Lexer import *
import Parser
from NodeVisitor import NodeVisitor

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
	# Returns a four-tuple of the form 'UNIT', e1, comp, e2 where
	# e1 and e2 are tuples representing eithing literals, variables
	# or keyword phrases
	#
	# @rtype: (String, Tuple, String, Tuple)
	def visit_Boolean(self, node):
		if node.op.type == EQUALS :
			return 'UNIT', (self.visit(node.e1), "==", self.visit(node.e2))
		elif node.op.type == LESSTHAN :
			return 'UNIT', (self.visit(node.e1), "<", self.visit(node.e2))
		elif node.op.type == GREATERTHAN :
			return 'UNIT', (self.visit(node.e1), ">", self.visit(node.e2))
		elif node.op.type == GREATEREQUAL :
			return 'UNIT', (self.visit(node.e1), ">=", self.visit(node.e2))
		elif node.op.type == LESSEQUAL :
			return 'UNIT', (self.visit(node.e1), "<=", self.visit(node.e2))

	## Visit Boolean Expression
	#
	# Returns a three tuple of the form b_left, op, b_right
	#
	# @rtype: (Tuple, String, Tuple)
	def visit_BoolExpr(self, node):
		if node.op:
			if node.op.type == AND:
				return node.bound, self.visit(node.left), "and", self.visit(node.right)
			elif node.op.type == OR:
				return node.bound, self.visit(node.left) , "or", self.visit(node.right)
		else:
			return self.visit(node.left)

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
			if arg in arg_indices:
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

	## Traverse Boolean Expression
	#
	#  Recursively descend Boolean Expression and appropriately print it out
	#
	#  @rtype: (String, String)
	def traverse_BoolExpr(self, cond, arg_indices):
		# if cond[1] is one of the comparative operators than we
		# know there is only one boolean statement (no && or ||)

		if not cond:
			return '', ''

		body = ''
		if_stmt = ''

		tab = '    '

		# if cond[1] in comps:
		if cond[0] == 'UNIT':
			body, if_stmt = self.compile_bool(cond[1], arg_indices)
			# Only add in tabs for body if there is a body
			if body != '':
				body = 2*tab + body
		else:
			# op  = the previous operand (either && or ||). It 
			#  		starts as 'if' for convenience sake as you'll
			#		see in the code below
			op = 'if'
			if isinstance(cond[0], bool):
				body, if_stmt = self.traverse_BoolExpr(cond[1:], arg_indices)
				if_stmt = if_stmt.replace('if ', 'if (')
				if_stmt = if_stmt.replace(':\n', '):\n')				
			else:
				body, if_stmt = self.traverse_BoolExpr(cond[0], arg_indices)
				body2 = if_stmt2 = ''
				if len(cond) > 1:
					op = cond[1]
					body2, if_stmt2 = self.traverse_BoolExpr(cond[2:], arg_indices)
					# Only add in tabs if the new addition to body 
					# is not empty
					if body2 != '':
						body += 2*tab+body2
					# Replace the ending colon and newline character with a
					# space for the previous if statement. Replace the 'if'
					# from the new if statement with the appropriate operand
					# (either 'and' or 'or'). Doing this allows us to have 
					# the whole conditional on one line, avoiding tabbing issues 
					if_stmt = if_stmt.replace(':\n',' ')+if_stmt2.replace('if', op)


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
			body, if_stmt2 = self.traverse_BoolExpr(cond, arg_indices)

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
