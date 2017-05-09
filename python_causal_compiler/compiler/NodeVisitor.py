## Node Visitor
#
#  @filename NodeVisitor.py
#  @author Ben Mariano
#  @date 5/9/2017
#
#  Visits all nodes of the AST by virtue of the visit_* methods
class NodeVisitor(object):
	## Visit
	#
	# @brief visits the AST node by calling the visit_'node' function
	#
	# @param node AST class to be evaluated
	# @retval object some object representation of the node
	def visit(self, node):
		method_name = 'visit_'+type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)

	## Visit Error
	#
	# @brief Alerts user if AST node has no defined visit function
	#
	# @param node AST class to be evaluated	
	def generic_visit(self, node):
		raise Exception('No visit_{} method'.format(type(node).__name__))
