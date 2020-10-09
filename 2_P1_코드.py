from parser import *	# should be copied


class Token:
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
		self.sourceFile = open(sourceFileName, 'r')

	def GetNextChar(self):
		"""
		Read a single character and convert it to lower case
		"""
		return self.sourceFile.read(1).lower()

	def PrintErrorMessage(message):
		"""
		Print an error message with prefix "E: "
		"""
		print("E: " + message)


class Scanner:
	"""
	The Scanner class recognizes and generates tokens 
	in a stream of characters and returns these tokens to the parser. 
	The Scanner class also detects any lexical errors.
	"""
	def __init__(self):
		print("haha")


class Parser:
	"""
	The Parser class uses a recursive descent strategy 
	to recognize phrases in a stream of tokens. Unlike the scanner, 
	which continues to generate tokens after lexical errors, 
	the parser halts execution upon encountering 
	the first syntax error in a source program.
	"""
	def __init__(self, chario, scanner):
		self.chario = chario
		self.scanner = scanner
		# should implement handles
		#self.initHandles()
		self.token = scanner.GetNextToken()


	def parse(self):
		self.subprogramBody()
		# accept EOF: check if extra symbols after logical end of program exist
		#self.accept(Token.EOF)


	def accept(self, expected, error_message):
		if self.token.code != expected:
			self.fatalError(error_message)
		self.token = self.scanner.GetNextToken()


	def fatalError(self, error_messager):
		self.chario.PrintErrorMessage(error_messager);
		raise RuntimeError("Fatal error")


	def subprogramBody(self):
		"""
		Check whole subprogram is match with EBNF grammar for TinyAda
		"""
		self.subprogramSpecification()

		if token != "is":
			PrintErrorMessage("is expected!")
		self.declarativePart()
		if GetNextToken() != "begin":
			PrintErrorMessage("begin expected!")
		self.sequenceOfStatements()
		if GetNextToken() != "end":
			PrintErrorMessage("end expected!")
		if PeekNextToken() != ";":
			self.ProcedureIdentifier()
		if GetNextToken() != ";":
			PrintErrorMessage("; expected!")

	def subprogramSpecification(self):
		"""

		"""
		if GetNextToken() != "procedure":
			PrintErrorMessage("procedure expected!")
		self.identifier()
		if 


if __name__ == "__main__":
	token = Token()
	chario = Chario("test.txt")
	scanner = Scanner()
	parser = Parser()

	while True:
		c = chario.GetNextChar()
		if not c:
			break
		else:
			print(c)

