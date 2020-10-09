from consts import *	# should be copied


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
		self.sourceFile = open(sourceFileName, 'rb')

	def GetNextChar(self):
		"""
		Read a single character and convert it to lower case
		"""
		raw = self.sourceFile.read(1)
		if raw == b'':
			return "EOF"
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


class Scanner:
	"""
	The Scanner class recognizes and generates tokens 
	in a stream of characters and returns these tokens to the parser. 
	The Scanner class also detects any lexical errors.
	"""
	def __init__(self, chario):
		self.chario = chario

	def PeekNextToken(self):
		return None

	def IntegerToken(self):
		"""
		Scans an integer value, which is a series of digits
		"""
		# print("scanning an integer token...")
		result = ""
		while self.chario.PeekNextChar().isdigit():
			result += self.chario.GetNextChar()

		return "int: " + result

	def AlphabeticToken(self):
		"""
		Scans either an identifier(e.g. variable name) or a reserved word(e.g. is, null).
		"""
		# print("scanning an alphabetic token...")
		# all possible alphabetic keywords(e.g. is, null, mod)
		reservedWords = pd.concat((reserved, basicDeclarationHandles, statementHandles, modOperator)).values

		# list of characters that cannot exist right after an identifier or a reserved word
		delimiters = (" ", "\n", "\r", "\t", "\\", ",", ":", "<", ">", "=", ";", "+", "-", "*", "/", "(", ")", "EOF")

		# scan the token
		result = ""
		while self.chario.PeekNextChar() not in delimiters:
			# print(self.chario.PeekNextChar() + " was not a delimiter")
			result += self.chario.GetNextChar()

		# print(self.chario.PeekNextChar() + " was a delimiter!")
	
		# return the result as either reserved word itself or an identifier
		if result in reservedWords:
			return result
		else:
			# return "id"
			return "id: " + result

	def OperatorToken(self):
		"""
		Scans an operator symbol from chario(e.g. +, :=).
		If an unexpected character is detected, RuntimeError will be raised.
		"""
		# print("scanning an operator token...")
		operators = pd.concat((addingOperator, multiplyingOperator, powerOperator, relationalOperator, tokenizer)).values
		validOperators = ("+", "-", "*", "/", "=", ":", ".", "(", ")", ",", "<", ">")

		if self.chario.PeekNextChar() == ";":
			return self.chario.GetNextChar()

		result = ""
		while self.chario.PeekNextChar() in validOperators:
			result += self.chario.GetNextChar()
		
		if result in operators:
			return result
		else:
			self.chario.PrintErrorMessage("Unexpected symbol '" + result + "'")

	def GetNextToken(self):
		"""
		Read characters from chario and return the first token found
		"""
		# print("scanning a token...")
		# remove space and newline
		ignoredCharacters = (" ", "\n", "\r", "\t", "\\")
		while True:
			nextChar = self.chario.PeekNextChar()
			# print("should I remove "+ nextChar+"?")
			if nextChar == "EOF":
				return "EOF"
			
			if nextChar in ignoredCharacters:
				self.chario.GetNextChar()
			else:
				break

		nextChar = self.chario.PeekNextChar()
		if nextChar.isalpha():
			return self.AlphabeticToken()
		elif nextChar.isdigit():
			return self.IntegerToken()
		else:
			return self.OperatorToken()


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
		self.chario.PrintErrorMessage(error_messager)
		raise RuntimeError("Fatal error")


	def subprogramBody(self):
		"""
		Check whole subprogram is match with EBNF grammar for TinyAda
		"""
		self.subprogramSpecification()
		self.accept(Token.IS, "\'" + Token.IS + "\' expected")
		self.declarativePart()
		self.accept(Token.BEGIN, "\'" + Token.BEGIN + "\' expected")
		self.sequenceOfStatements()
		self.accept(Token.END, "\'" + Token.END + "\' expected")
		if token.code == Token.ID:
			self.token = scanner.GetNextToken()
		self.accept(Token.SEMI, "semicolon expected")

	def declarativePart():
		while token.code in Token.basicDeclarationHandles:
			self.basicDeclaration()

	def basicDeclaration():
		if token.code == Token.ID:
			self.numberOrObjectDeclaration()
 		elif self.token.code == Token.TYPE:
 			self.typeDeclaration()
 		elif self.token.code == Token.PROC:
 			self.subprogramBody()
 		else:
 			self.fatalError("error in declaration part")


	def subprogramSpecification(self):
		self.accept(Token.PROC, "procedure expected!")
		self.identifier()
		if self.token.code == "(":	# note
			self.formalPart()



	
	def expression(self):
		self.relation()
		while self.token.code == Token.AND or 
				self.token.code == Token.OR:
			self.token = self.scanner.GetNextToken()
			self.relation()


	def relation(self):
		self.simpleExpression()
		if self.token.code in Token.relationalOperator:
			self.token = self.scanner.GetNextToken()
			self.simpleExpression()


	def simpleExpression(self):
		if self.token.code in Token.addingOperator:
			self.token = self.scanner.GetNextToken()
		self.term()
		while self.token.code in Token.addingOperator:
			self.token = self.scanner.GetNextToken()
			self.term();

	def term(self):
		self.factor()
		while self.token in Token.multiplyingOperator:
			self.token = self.scanner.GetNextToken()
			self.factor()


	def factor(self):
		self.primary():
		if self.token.:
			pass


if __name__ == "__main__":
	chario = Chario("test.txt")
	scanner = Scanner(chario)

	# while True:
	# 	peek = chario.PeekNextChar()
	# 	print("Peek: " + peek)
	# 	if peek != "EOF":
	# 		print(chario.GetNextChar())
	# 	else:
	# 		break
	# while chario.PeekNextChar() not in ("EOF"):
		# print(chario.GetNextChar())

	# while True:
		# print(chario.PeekNextChar())
		# chario.GetNextChar()

	# print(scanner.GetNextToken())

	while True:
		token = scanner.GetNextToken()
		print("token: " + token)
		if token == "EOF":
			break

# 	token = Token()
# 	chario = Chario("test.txt")
# 	scanner = Scanner()
# 	parser = Parser()

# 	while True:
# 		c = chario.GetNextChar()
# 		if not c:
# 			break
# 		else:
# 			print(c)

