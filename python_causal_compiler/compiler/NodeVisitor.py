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
