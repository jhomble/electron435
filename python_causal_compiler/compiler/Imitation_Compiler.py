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
		#  variable equivalents per method
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
		ret = '__ret_val = ['

		# iterate through each action adding it and its 
		# arguments to the return string
		for action in acts:
			ret += '(\''+action[0]+'\','
			for a in range(0, len(action[1])):
				arg = action[1][a]
				if arg[:4] == 'CONT':
					if not self.method_var_equivs.has_key(act_name):
						self.method_var_equivs[act_name] = {}
					prev_arg = action[1][a-1]
					'TODO: THIS COULD CAUSE COLLISION ERROR'
					self.method_var_equivs[act_name][arg] = prev_arg					
				ret += '#'+arg + ','
			ret = ret[:len(ret)-1] + ')'
			ret += ','

		ret = ret[:len(ret)-1] + ']\n'

		ret += 'return __ret_val\n' 

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
						for i in range(index, len(intention_Args)):
							prev_arg_2 = intention_Args[i]
							if not self.method_var_equivs.has_key(act_name):
								self.method_var_equivs[act_name] = {}
							new_index = i - index
							self.method_var_equivs[act_name][prev_arg_2] = prev_arg+'['+str(new_index)+']'
						if not self.method_var_equivs.has_key(act_name):
							self.method_var_equivs[act_name] = {}
						self.method_var_equivs[act_name][prev_arg] = prev_arg +'[0]'
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

		if (self.method_var_equivs.has_key(self.intention)):
			self.method_var_equivs[self.intention].update(var_equiv)
		else:
			self.method_var_equivs[self.intention] = var_equiv

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
				obj_id = expr1[1]+'_id'
				body += 'all_'+expr1[1]+' = ['+obj_id+' for '
				body += obj_id+' in state.objs if state.objs['+obj_id
				body += '][0]==\''+expr1[1]+'\']\n'
				body += 'if True:\n'
				for a in range(0, len(expr2)):
					arg = expr2[a]
					if arg[:4] == 'CONT':
						cont_offset = int(arg[4:])
						self.method_var_equivs[self.intention][arg] = ')+tuple(all_'+expr1[1]+'['+str(a-cont_offset)+':]'
					else:
						self.method_var_equivs[self.intention][arg] = 'all_'+expr1[1]+'['+str(a)+']'
			elif expr1[0] == 'TYPE':
				var_name = expr1[1]
				var_name = '#'+expr1[1]
				if_stmt += 'if state.objs['+var_name+'][0] == \''
				if_stmt += expr2+'\':\n'
			else:
				# var1 and var2 could be either variables or literals
				var1 = ''
				var2 = ''
				isVar1Lit = False
				isVar2Lit = False

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
				elif not isVar1Lit and not isVar2Lit:
					var1_star = '*'+var1
					var2_star = '*'+var2
					real_var = ''
					temp_var = ''
					if var1 in intention_Args:
						real_var = var1
						temp_var = var2
					elif var1_star in intention_Args:
						'TODO: Update this'
						real_var = var1 + '[0]'
						temp_var = var2						
					elif var2 in intention_Args:
						real_var = var2
						temp_var = var1											
					elif var2_star in intention_Args:
						'TODO: Update this'
						real_var = var2 + '[0]'
						temp_var = var1
					elif var_equiv.has_key(var1):
						real_var = var_equiv[var1]
						temp_var = var2
					elif var_equiv.has_key(var2):
						real_var = var_equiv[var2]
						temp_var = var1
					else:
						raise Exception('Variables '+var1+','+var2+' were not found!')

					var_equiv[temp_var] = real_var
				else:
					lit_var = ''
					real_var = ''
					if isVar1Lit:
						lit_var = var1
						real_var = var2
					else:
						lit_var = var2
						real_var = var1

					var_equiv[real_var] = lit_var

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

		print('Vars Dict:')
		for intent in self.method_var_equivs:
			print('\tIntention: '+str(intent))
			int_dict = self.method_var_equivs[intent]
			for var in int_dict:
				if 'CONT' in var:
					if self.method_var_equivs[intent].has_key(int_dict[var]):
						old_val = self.method_var_equivs[intent][int_dict[var]]
						old_index = old_val[len(old_val)-2]
						new_index = int(old_index)+1
						cont_offset = int(var[4:])
						new_index = str(new_index - cont_offset)
						new_val = ')+tuple('+old_val.replace(old_index+']', new_index+':]')
						self.method_var_equivs[intent][var] = new_val
				print('\t\tdict['+var+'] ='+int_dict[var])

		for intention in self.methods_dict:
			args = self.methods_dict[intention][0]
			conds = self.methods_dict[intention][1]
			rets = self.methods_dict[intention][2]
			for c in range(0, len(conds)):
				cond = conds[c]
				if self.method_var_equivs.has_key(intention):
					for var in self.method_var_equivs[intention]:

						cond = cond.replace('#'+var, self.method_var_equivs[intention][var])

				if cond:
					cond = cond.replace('#', '')
					conds[c] = cond				
			for r in range(0, len(rets)):
				ret = rets[r]
				if self.method_var_equivs.has_key(intention):
					for var in self.method_var_equivs[intention]:
						if 'CONT' in var and var in ret:
							cont_offset = int(var[4:]) + 1
							temp_ret = ret
							temp_ret = temp_ret.split('#'+var)
							temp_ret = temp_ret[0][::-1]
							index = -1
							for i in range(0, len(temp_ret)):
								c = temp_ret[i]
								if c == ',':
									index = i
									cont_offset -= 1
								if cont_offset == 0:
									break
							var_index = ret.find('#'+var)
							print('RETURN:')
							print(ret[var_index-index:var_index])
							ret = ret[0:var_index-index]+ret[var_index:]
						ret = ret.replace('#'+var, self.method_var_equivs[intention][var])
				if ret:
					ret = ret.replace('#', '')
					rets[r] = ret				

		for intention in self.methods_dict:
			args = self.methods_dict[intention][0]
			conds = self.methods_dict[intention][1]
			rets = self.methods_dict[intention][2]
			method_dec = 'def '
			intention_no_hyphen = intention.replace('-', '_')
			method_dec += intention_no_hyphen
			method_dec += '(state'
			objs_conv = ''
			for arg in args:
				method_dec += ', '+arg
				if arg[0] == '*':
					objs_conv = tab+arg[1:]+' = flatten('+arg[1:]+')\n'
			method_dec += '):\n'
			pyhop_stmt = 'pyhop.declare_methods(\''+intention+'\','
			pyhop_stmt += intention_no_hyphen+')\n'
			result += method_dec
			result += objs_conv
			red_check = ''			
			ret1_tabs = tab
			ret2_tabs = tab
			if len(rets) > 1:
				'TODO: Multiple possible reductions!'
				ret2_tabs += tab
				red_check = 2*tab+'__all_args = []\n'
				red_check += 2*tab+'for __action in __ret_val:\n'
				red_check += 3*tab+'for __arg in __action:\n'
				#red_check += 4*tab+'if isinstance(__arg, list):\n'
				# red_check += 5*tab+'for i in __arg:\n'
				# red_check += 6*tab+'__all_args.append(__arg)\n'
				# red_check += 4*tab+'else:\n'
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
				# num_newlines = red_check.count('\n')
				#red_check = red_check.replace('\n', '\n'+tab, num_newlines-1)
			for i in range(0, len(rets)):
				ret = rets[i]
				cond = conds[i]
				ret1_temp = ret1_tabs
				ret2_temp = ret2_tabs
				if cond:
					if 'if' in cond and ':\n' in cond:
						print('RET: '+ret)
						print('\t'+cond)
						ret1_temp += tab
						ret2_temp += tab
					num_newlines = cond.count('\n')
					result += tab + cond.replace('\n', '\n'+tab, num_newlines-1)
				ret_lines = ret.split('\n')
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
