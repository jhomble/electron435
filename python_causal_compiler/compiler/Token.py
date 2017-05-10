## Token Class
#
#  @filename Token.py
#  @author Ben Mariano
#  @date 5/9/2017
#
#  @brief A Token object represents a slightly abstracted piece of syntax
#  from the custom language
class Token(object):
	## Constructor
	#
	#  @param type possible token type: VAR, COMMA, CAUSES, etc.
	#  @param value possible token value: int, float, string, ...
	def __init__(self, type, value):
		## @var type
		# possible token type: VAR, COMMA, CAUSES, etc.
		self.type = type
		## @var value
		# possible token value: int, float, string, None
		self.value = value

	## To String
	#
	# @retval String 
	def __str__(self):

		return 'Token({type}, {value})'.format(
			type = self.type,
			value = repr(self.value)
		)

	def __repr__(self):
		return self.__str__()
