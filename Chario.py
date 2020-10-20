class Chario:
	"""
	The Chario class (short for character I/O) converts
	the source program’s text into a stream of characters for the scanner,
	thus enabling the scanner to focus on lexical analysis
	rather than low-level text processing.
	The Chario class also handles the output of any error messages.
	"""

	def __init__(self, sourceFileName):
		"""
		open an Ada source file(.txt extension)
		"""
		self.sourceFile = open(sourceFileName, 'rb')


	def GetNextChar(self):
		"""
		Read a single character and convert it to lower case
		"""
		escapeSequence = {b'\n' : "\n", b'\t' : "\t", b'\r' : "\r"}

		raw = self.sourceFile.read(1)
		if raw == b'':
			return "EOF"
		elif raw in escapeSequence:
			return escapeSequence[raw]
		else:
			return str(raw)[2:3].lower()


	def PeekNextChar(self):
		"""
		Read a single character without changing file pointer
		"""
		rtn = self.GetNextChar()
		if rtn != "EOF":
			self.sourceFile.seek(-1, 1)

		return rtn

	def PrintErrorMessage(self, message):
		"""
		Print an error message with prefix "E: "
		"""
		print("E: " + message)
