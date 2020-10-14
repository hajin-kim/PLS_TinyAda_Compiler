from Const import Const


class Token(Const):
	"""
	The Token class represents tokens in the language.
	For simple syntax analysis, a token object need only
	include a code for the token’s type,
	such as was used in earlier examples in this chapter.
	However, a token can include other attributes,
	such as an identifier name, a constant value,
	and a data type, as we will see in later chapters.
	"""

	def __init__(self, code, value):
		self.code = code
		self.value = value

	
	def __str__(self):
		if self.code == Const.NEWLINE:
			return "[newline]"
		
		name = "[" + self.code
		if self.code in (Const.numericalLiteral, Const.ID):
			name += "(" + self.value + ")"
		name += "]"
		return name

