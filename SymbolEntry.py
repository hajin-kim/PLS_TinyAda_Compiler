class SymbolEntry(object):
	"""docstring for SymbolEntry"""

	CONST = "const"
	VAR = "var"
	TYPE = "type"
	PROC = "proc"
	PARAM = "param"

	def __init__(self, name, role=None, value=None):
		super(SymbolEntry, self).__init__()
		self.name = name.lower() if name.__class__ == "str" else name
		self.role = role
		self.value = value




		