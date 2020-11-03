from SymbolEntry import SymbolEntry

class SymbolTable(object):
	"""docstring for SymbolTable"""

	def __init__(self, chario):
		"""
		Creates an empty stack of tables, with a reference to a Chario object for the output of error messages.
		
		Arguments:
			chario {Chario} -- the main Chario instance
		"""
		self.chario = chario
		self.stack = []
		

	def enterScope(self):
		"""
		Pushes a new table onto the stack.
		"""
		self.stack.append([])


	def exitScope(self):
		"""
		Pops a table from the stack and prints its contents.
		"""
		self.stack.pop()


	def enterSymbol(self, name, role=None, value=None):
		"""
		If name is not already present, inserts an entry for it into the
		table and returns that entry; otherwise, prints an error message
		and returns an empty entry.
		
		Arguments:
			name {str} -- the name of the new symbol(identifier)
		
		Returns:
			[SymbolEntry, None] -- the new entry instance
		"""
		name = name.lower()
		if name in [entry.name for entry in self.stack[-1]]:
			self.chario.PrintErrorMessage("redefinition of already defined identifier [" + name + "]")
			return None
		newEntry = SymbolEntry(name, role, value)
		self.stack[-1].append(newEntry)
		return newEntry


	def findSymbol(self, name):
		"""
		If name is already present, returns its entry; otherwise, prints
		an error message and returns an empty entry.
		
		Arguments:
			name {str} -- the name of the entry to find
		
		Returns:
			[SymbolEntry, None] -- the entry found
		"""
		if name == None:
			return None
			
		name = name.lower()
		for scope in self.stack[::-1]:
			for entry in scope:
				if name == entry.name:
					return entry
		self.chario.PrintErrorMessage("undefined identifier [" + name + "] was used")
		return None





















