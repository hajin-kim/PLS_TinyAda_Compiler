class SymbolEntry(object):
	"""docstring for SymbolEntry"""

	CONST = "const"
	VAR = "var"
	TYPE = "type"
	PROC = "proc"
	PARAM = "param"

	def __init__(self, name):
		super(SymbolEntry, self).__init__()
		self.name = name
		self.role = None


		