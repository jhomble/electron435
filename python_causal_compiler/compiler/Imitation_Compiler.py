## Imitation Compiler

# Library Imports
import operator
import functools

# Local Imports
import Token
from Lexer import *
import Parser
from NodeVisitor import NodeVisitor

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
		## @var method_var_equivs
		#  Variable equivalents per method. This keeps track of which
		#  variable must be equal based on conditionals.
		self.method_var_equivs = {}

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

		return acts

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

		# return statement
		#    defines return value as variable then returns this variable
		ret = '__ret_val = ['

		# iterate through each action adding it and its 
		# argument placeholders to the return string
		for action in acts:
			ret += '(\''+action[0]+'\','
			# iterate through each argument to an action
			for a in range(0, len(action[1])):
				arg = action[1][a]
				# Handle the special case of the CONT keyword
				if arg[:4] == 'CONT':
					# create a dictionary for act_name intention
					# in the method_var_equivs if it's not there
					if not act_name in self.method_var_equivs:
						self.method_var_equivs[act_name] = {}
					prev_arg = action[1][a-1]
					# adjust arg name to avoid collisions
					arg = arg + "-" + prev_arg
					self.method_var_equivs[act_name][arg] = prev_arg					
				# use hashtag notation to indicate arg_name to be replaced
				ret += '#'+arg + ','
			ret = ret[:len(ret)-1] + ')'
			ret += ','

		# add final bracket to return array
		ret = ret[:len(ret)-1] + ']\n'

		# add return statement with the return value
		ret += 'return __ret_val\n' 

		# Check if method has already been defined
		if act_name in self.methods_dict:
			args, conds, rets = self.methods_dict[act_name]
			# Check if you have to change parameters (add final *)
			if len(intention_Args) > len(args):
				prev_arg = ''		
				# iterate through intention args		
				for a in range(0, len(intention_Args)):
					arg = intention_Args[a]
					# handle CONT keyword
					if arg[:4] == 'CONT':
						# Get argument referenced by CONT number
						index = a - int(arg[4:])
						prev_arg = args[index]
						# iterate through intention args coming after the first item
						# referenced by the CONT
						for i in range(index, len(intention_Args)):
							prev_arg_2 = intention_Args[i]
							# check if there's an entry yet for this intention
							if not act_name in self.method_var_equivs:
								self.method_var_equivs[act_name] = {}
							new_index = i - index
							# add in new mapping for each of the args in CONT list
							self.method_var_equivs[act_name][prev_arg_2] = prev_arg+'['+str(new_index)+']'
						if not act_name in self.method_var_equivs:
							self.method_var_equivs[act_name] = {}
						# Map first arg in CONT list
						self.method_var_equivs[act_name][prev_arg] = prev_arg +'[0]'
						# Use star notation to indicate that the method arguments needs
						# star at the end to indicate variable length tuple in Python
						prev_arg = '*' + prev_arg
				adjusted_args = args
				adjusted_args[index] = prev_arg
				self.methods_dict[act_name] = (adjusted_args, conds, rets)

			# Update Methods Dict
			self.methods_dict[act_name][2].append(ret)
		else:
			self.methods_dict[act_name] = (intention_Args, [], [ret])

		return act_name

	## Visit No Conditional
	#
	# Return None when there is no conditional
	def visit_NoCond(self,node):
		return None

	## Traverse Boolean Expression
	#
	#  Recursively descend Boolean Expression and appropriately print it out
	#
	#  @rtype: (String, String)
	def traverse_BoolExpr(self, cond):
		# if cond[1] is one of the comparative operators than we
		# know there is only one boolean statement (no && or ||)

		print('Traversing: '+str(cond))

		if not cond:
			return '', ''

		body = ''
		if_stmt = ''

		tab = '    '

		# if cond[1] in comps:
		if cond[0] == 'UNIT':
			body, if_stmt = self.compile_bool(cond[1])
			# Only add in tabs for body if there is a body
			if body != '':
				# body = 2*tab + body
				body = body
		else:
			# op  = the previous operand (either && or ||). It 
			#  		starts as 'if' for convenience sake as you'll
			#		see in the code below
			op = 'if'
			if isinstance(cond[0], bool):
				'TODO'
				body, if_stmt = self.traverse_BoolExpr(cond[1:])
				if_stmt = if_stmt.replace('if ', 'if (')
				if_stmt = if_stmt.replace(':\n', '):\n')				
			else:
				body, if_stmt = self.traverse_BoolExpr(cond[0])
				print('COND: '+str(cond))
				body2 = if_stmt2 = ''
				if len(cond) > 1:
					op = cond[1]
					body2, if_stmt2 = self.traverse_BoolExpr(cond[2:])
					# Only add in tabs if the new addition to body 
					# is not empty
					if body2 != '':
						# body += 2*tab+body2
						body += body2
					# Replace the ending colon and newline character with a
					# space for the previous if statement. Replace the 'if'
					# from the new if statement with the appropriate operand
					# (either 'and' or 'or'). Doing this allows us to have 
					# the whole conditional on one line, avoiding tabbing issues 
					if_stmt = if_stmt.replace(':\n',' ')+if_stmt2.replace('if', op)


		return body, if_stmt

	## Visit Conditional
	#
	#  Return the result of evaluating the boolean expression
	def visit_Cond(self, node):
		result = ''

		boolean = self.visit(node.boolean)

		# Comparative Operators in Custom Language
		comps = ['==', '<', '>', '<=', '>=']

		# body     = Additional things added to the body of if_stmt.
		#			 This could include calls to lookup_type or
		#			 defining local variables
		# if_stmt  = Handles conditional relationship rules. For
		#			 example, this if statement would include
		#   		 checking the type of an object		
		if_stmt = ''
		body = ''
		paren = ''

		# Only evaluate conditional if there are any
		if boolean:
			body, if_stmt = self.traverse_BoolExpr(boolean)
			# # if boolean[1] is one of the comparative operators than we
			# # know there is only one boolean statement (no && or ||)
			# if boolean[1] in comps:
			# 	body, if_stmt = self.compile_bool(boolean, '', '')
			# else:
			# 	# op  = the previous operand (either && or ||). It 
			# 	#  		starts as 'if' for convenience sake as you'll
			# 	#		see in the code below
			# 	op = 'if'
			# 	# Go through each boolean statement
			# 	for i in range(0, len(boolean)):
			# 		# change the operand appropriately to reflect which op it is
			# 		if len(boolean[i]) > 0:
			# 			if boolean[i] == ')' or boolean[i][0] == '(':
			# 				paren += boolean[i]
			# 			else:
			# 				if boolean[i] == '&&':
			# 					op = 'and'
			# 				elif boolean[i] == '||':
			# 					op = 'or'
			# 				else:
			# 					body2, if_stmt2 = self.compile_bool(boolean[i], op, paren)
			# 					# Only add in tabs if the new addition to body 
			# 					# is not empty
			# 					if body2 != '':
			# 						body += body2
			# 					# Replace the ending colon and newline character with a
			# 					# space for the previous if statement. Replace the 'if'
			# 					# from the new if statement with the appropriate operand
			# 					# (either 'and' or 'or'). Doing this allows us to have 
			# 					# the whole conditional on one line, avoiding tabbing issues
			# 					if if_stmt2 != '': 
			# 						if_stmt = if_stmt.replace(':\n',' ')+if_stmt2.replace('if', op)

		print('HERE1: '+str(body))								
		print('HERE2: '+str(if_stmt))										

		result += body + if_stmt

		return result

	## Handle Type Keyword
	#
	#  Returns a string representing the updated if statement for
	#  the type keyword
	#
	#  @rtype: String
	def handle_Type(self, expr, arg_num, if_stmt):
		# Handles arg 1 and 2 slightly differently
		if arg_num == 1:
			var_name = '#'+expr
			if_stmt += 'if state.objs['+var_name+'][0] == '				
		elif arg_num == 2:
			var_name = '#'+expr
			if_stmt += 'state.objs['+var_name+'][0]:\n'				
		else:
			raise Exception('There can only be one expression on either side of an equality comparator!')

		return if_stmt

	## Compile Boolean Statement
	#
	# Returns a tuple (body, if statement) that represents the 
	# required additions to the output to succesffuly match the 
	# conditional.
	#
	# @rtype: (String, String)
	def compile_bool(self, cond):
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

		# Retrieve the intention arguments from the dictionary
		#   NOTE: It is known at this point that there is an entry
		#		  for self.intention in the dictionary
		intention_Args = self.methods_dict[self.intention][0]

		# Check comparator type
		if comp == '==':
			# Evaluate All Keyword
			if expr1[0] == 'ALL':
				# define body statement
				obj_id = expr1[1]+'_id'
				body += 'all_'+expr1[1]+' = ['+obj_id+' for '
				body += obj_id+' in state.objs if state.objs['+obj_id
				body += '][0]==\''+expr1[1]+'\']\n'
				# add this if statement to preserve appropriate tabbing
				if_stmt += 'if True:\n'
				# items in second expression list
				#   NOTE: expr2 must be a list
				for a in range(0, len(expr2)):
					arg = expr2[a]
					# Handle CONT keyword
					if arg[:4] == 'CONT':
						cont_offset = int(arg[4:])
						prev_arg = expr2[a-cont_offset]
						# alter arg name to avoid namespace collision
						arg = arg + '-' + prev_arg
						self.method_var_equivs[self.intention][arg] = ')+tuple(all_'+expr1[1]+'['+str(a-cont_offset)+':]'
					else:
						self.method_var_equivs[self.intention][arg] = 'all_'+expr1[1]+'['+str(a)+']'
			# evaluate TYPE keyword
			elif expr1[0] == 'TYPE':
				if_stmt = self.handle_Type(expr1[1], 1, if_stmt)
				# the second expression is known to be either a literal
				# or another TYPE expression
				if expr2[0] == 'TYPE':
					if_stmt = self.handle_Type(expr2[1], 2, if_stmt)	
				else:
					if_stmt += '\''+expr2+'\':\n'
			# Handle variable/literal comparison
			else:
				if_stmt += 'if True:\n'				
				# var1 and var2 could be either variables or literals
				var1 = ''
				var2 = ''
				isVar1Lit = False
				isVar2Lit = False

				# Add quotes around literals and determine which vars
				# are literals
				if expr1[0] == 'LITERAL':
					var1 = '\''+str(expr1[1])+'\''
					isVar1Lit = True
				else:
					var1 = expr1
				if expr2[0] == 'LITERAL':
					var2 = '\''+str(expr2[1])+'\''
					isVar2Lit = True
				else:
					var2 = expr2

				if isVar1Lit and isVar2Lit:
					raise Exception('Comparing '+var1+' and '+var2+' which are both String literals!')
				# They are both variables
				elif not isVar1Lit and not isVar2Lit:
					var1_star = '*'+var1
					var2_star = '*'+var2
					real_var = ''
					temp_var = ''

					# The 'real_var' is the one present in the intention, i.e.
					# the method args. References to the 'temp_var' should 
					# be replaced with the 'real_var'. Make sure to also check
					# for the starred variables and check for equivalents in the
					# method_var_equivs dictionary.
					if var1 in intention_Args:
						real_var = var1
						temp_var = var2
					elif var1_star in intention_Args:
						# The star always refers to the 0 index
						real_var = var1 + '[0]'
						temp_var = var2						
					elif var2 in intention_Args:
						real_var = var2
						temp_var = var1											
					elif var2_star in intention_Args:
						# The star always refers to the 0 index
						real_var = var2 + '[0]'
						temp_var = var1
					elif var1 in self.method_var_equivs[self.intention]:
						real_var = self.method_var_equivs[self.intention][var1]
						temp_var = var2
					elif var2 in self.method_var_equivs[self.intention]:
						real_var = self.method_var_equivs[self.intention][var2]
						temp_var = var1
					else:
						raise Exception('Variables '+var1+','+var2+' were not found!')

					self.method_var_equivs[self.intention][temp_var] = real_var
				# one variable is literal, one isn't
				else:
					lit_var = ''
					real_var = ''
					# determine which is the literal and assign locals
					# appropriately
					if isVar1Lit:
						lit_var = var1
						real_var = var2
					else:
						lit_var = var2
						real_var = var1

					self.method_var_equivs[self.intention][real_var] = lit_var

		else:
			raise Exception('\''+str(comp)+'\' comparator currently not supported')

		return body, if_stmt

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

		# Define standard tab
		tab = '    '

		# iterate through intentions in the method_var_equivs
		for intent in self.method_var_equivs:
			int_dict = self.method_var_equivs[intent]
			# iterate through the variables in the method_var_equivs at a 
			# given intention
			for var in int_dict:
				# Only make changes if one of the vars is CONT
				if 'CONT' in var:
					# Check for/update value mapped to CONT and update it
					if int_dict[var] in self.method_var_equivs[intent]:
						old_val = self.method_var_equivs[intent][int_dict[var]]
						old_index = old_val[len(old_val)-2]
						new_index = int(old_index)+1
						cont_offset = int(var[4:var.find('-')])
						new_index = str(new_index - cont_offset)
						new_val = ')+tuple('+old_val.replace(old_index+']', new_index+':]')
						self.method_var_equivs[intent][var] = new_val

		# Iterate through each intention in the methods dictionary
		for intention in self.methods_dict:
			args = self.methods_dict[intention][0]
			conds = self.methods_dict[intention][1]
			rets = self.methods_dict[intention][2]
			# Iterate through the conditions
			for c in range(0, len(conds)):
				cond = conds[c]
				# Replace all variables with dictionary equivalent if it exists
				if intention in self.method_var_equivs:
					for var in self.method_var_equivs[intention]:

						cond = cond.replace('#'+var, self.method_var_equivs[intention][var])
				# Remove remaining unnecessary hashtags
				if cond:
					cond = cond.replace('#', '')
					conds[c] = cond				
			# Iterate through the return statements
			for r in range(0, len(rets)):
				ret = rets[r]
				# Replace all variables with their dictionary equivalents 
				if intention in self.method_var_equivs:
					for var in self.method_var_equivs[intention]:
						# Handle CONT keyword
						if 'CONT' in var and var in ret:
							cont_offset = int(var[4:var.find('-')]) + 1
							temp_ret = ret
							temp_ret = temp_ret.split('#'+var)
							temp_ret = temp_ret[0][::-1]
							index = -1
							# Find index of ',' which denotes the end
							# of the argument in question
							for i in range(0, len(temp_ret)):
								c = temp_ret[i]
								if c == ',':
									index = i
									cont_offset -= 1
								if cont_offset == 0:
									break
							var_index = ret.find('#'+var)
							ret = ret[0:var_index-index]+ret[var_index:]
						ret = ret.replace('#'+var, self.method_var_equivs[intention][var])
				# Remove unnecessary hashtags
				if ret:
					ret = ret.replace('#', '')
					rets[r] = ret				

		# Iterate through the now updated methods dictionary
		for intention in self.methods_dict:
			args = self.methods_dict[intention][0]
			conds = self.methods_dict[intention][1]
			rets = self.methods_dict[intention][2]
			# Build method declaration string
			method_dec = 'def '
			# python functions cannot have hyphens :(
			intention_no_hyphen = intention.replace('-', '_')
			method_dec += intention_no_hyphen
			method_dec += '(state'
			objs_conv = ''
			# Iterate through method args and print
			for arg in args:
				method_dec += ', '+arg
				# identify the presence of the * in the args
				# if it's there define the flatten call which will
				# convert the multiple layer tuple into a single
				# layer array/tuple
				if arg[0] == '*':
					objs_conv = tab+arg[1:]+' = flatten('+arg[1:]+')\n'
			method_dec += '):\n'
			pyhop_stmt = 'pyhop.declare_methods(\''+intention+'\','
			pyhop_stmt += intention_no_hyphen+')\n'
			result += method_dec
			result += objs_conv
			# Reduction check, includes all of the conditional obligations
			# required when there are multiple reductions
			red_check = ''			
			# tabbing for the first return
			ret1_tabs = tab
			# tabbing for the second return
			ret2_tabs = tab
			# Check if there are multiple possible reductions
			if len(rets) > 1:
				# This adds in a check which reduction should be used by creating a
				# a comparitive statement that checks if the arguments in the return
				# contains all the arguments passed into the function
				ret2_tabs += tab
				red_check = 2*tab+'__all_args = []\n'
				red_check += 2*tab+'for __action in __ret_val:\n'
				red_check += 3*tab+'for __arg in __action:\n'
				red_check += 4*tab+'__all_args.append(__arg)\n'
				red_check += 2*tab+'__all_intention_args = ['
				for arg in args:
					if arg[0] == '*':
						red_check += '[__obj for __obj in '+arg[1:]+']'
					else:
						red_check += '['+arg + '],'
				red_check += ']\n'
				red_check += 2*tab+'__all_intention_args = flatten(__all_intention_args)\n'
				red_check += 2*tab+'__all_args = flatten(__all_args)\n'				
				red_check += 2*tab+'if set(__all_intention_args).issubset(set(__all_args)):\n'
			# Iterate through return statements
			for i in range(0, len(rets)):
				ret = rets[i]
				cond = conds[i]
				ret1_temp = ret1_tabs
				ret2_temp = ret2_tabs
				# adjust tabbing for condition and add it in
				if cond:
					if 'if' in cond and ':\n' in cond:
						ret1_temp += tab
						ret2_temp += tab
					num_newlines = cond.count('\n')
					result += tab + cond.replace('\n', '\n'+tab, num_newlines-1)
				ret_lines = ret.split('\n')
				# add actual returns, split in case there are two possible returns
				'TODO: HANDLE MORE THAN TWO RETURNS?'
				result += ret1_temp + ret_lines[0] + '\n'
				result += red_check
				result += ret2_temp + ret_lines[1] + '\n'
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
		flt = self.visit(node.left) + '.' + self.visit(node.right)
		print('FLOAT: '+flt)
		return flt

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
