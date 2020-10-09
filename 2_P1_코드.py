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
		if token.code == Token.ID:	# force <procedure>identifier
			self.token = scanner.GetNextToken()
		self.accept(Token.SEMI, "semicolon expected")

	def declarativePart(self):
		while token.code in Token.basicDeclarationHandles:
			self.basicDeclaration()

	def basicDeclaration(self):
		if token.code == Token.ID:
			self.numberOrObjectDeclaration()
 		elif self.token.code == Token.TYPE:
 			self.typeDeclaration()
 		elif self.token.code == Token.PROC:
 			self.subprogramBody()
 		else:
 			self.fatalError("error in declaration part")

 	def objectDeclaration(self):
 		self.identifierList()
 		self.accept(Token.COLON,"\'" + Token.COLON + "\' expected")
 		self.typeDeclaration()
 		self.accept(Token.SEMICOLON,"\'" + Token.SEMICOLON + "\' expected")

 	def numberDeclaration(self);
 		self.identifierList()
 		self.accept(Token.COLON,"\'" + Token.COLON + "\' expected")
 		self.accept("constant","\'" + "constant" + "\' expected")
 		self.accept(Token.COLON_EQ,"\'" + Token.COLON_EQ + "\' expected")
 		self.expression()
 		self.accept(Token.SEMICOLON,"\'" + Token.SEMICOLON + "\' expected")

 	def identifierList(self):
 		self.accept(Token.ID, "identifier expected")
 		while self.token.code == Token.COMMA:
 			self.token = self.scanner.GetNextToken()
			self.accept(Token.ID, "identifier expected")

	def typeDeclaration(self):
		self.accept(Token.TYPE,"\'" + Token.TYPE + "\' expected")
		self.accept(Token.ID, "identifier expected")
		self.accept(Token.IS, "\'" + Token.IS + "\' expected")
		self.typeDefinition()
		self.accept(Token.SEMICOLON,"\'" + Token.SEMICOLON + "\' expected")

	def typeDefinition(self):
		if token.code == Token.PARENTHESIS_OPEN:
			self.enumerationTypeDefinition()
		elif token.code == Token.ARRAY:
			self.arrayTypeDefinition()
		elif token.code == Token.RANGE:
			self.range()
		else:
			self.name()

	def range(self):
		self.accept(Token.IS, "\'" + Token.IS + "\' expected")
		self.simpleExpression()
		self.accept(Token.DOT_DOT, "\'" + Token.DOT_DOT + "\' expected")
		self.simpleExpression()

	def index(self):
		if token.code == Token.RANGE:
			self.range()
		else:
			self.name()

	def enumerationTypeDefinition(self):
		self.accept(Token.PARENTHESIS_OPEN, "\'" + Token.PARENTHESIS_OPEN + "\' expected")
		self.identifierList()
		self.accept(Token.PARENTHESIS_CLOSE, "\'" + Token.PARENTHESIS_CLOSE + "\' expected")
	
	def arrayTypeDefinition(self):
		self.accept(Token.ARRAY, "\'" + Token.ARRAY + "\' expected")
		self.accept(Token.PARENTHESIS_OPEN, "\'" + Token.PARENTHESIS_OPEN + "\' expected")
		self.index()
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			self.index()
		self.accept(Token.PARENTHESIS_CLOSE, "\'" + Token.PARENTHESIS_CLOSE + "\' expected")
		self.accept(Token.OF, "\'" + Token.OF + "\' expected")
		self.name()

	def subprogramSpecification(self):
		self.accept(Token.PROC, "procedure expected!")
		self.accept(Token.ID, "identifier expected")
		if self.token.code == "(":	# note
			self.formalPart()

	def formalPart(self):
		self.accept(Token.PARENTHESIS_OPEN, "\'" + Token.PARENTHESIS_OPEN + "\' expected")
		self.parameterSpecification()
		while self.token.code == Token.SEMICOLON:
			self.token = self.scanner.GetNextToken()
			self.parameterSpecification()
		self.accept(Token.PARENTHESIS_CLOSE, "\'" + Token.PARENTHESIS_CLOSE + "\' expected")

	def parameterSpecification(self):
		self.identifierList()
		self.accept(Token.COLON, "\'" + Token.COLON + "\' expected")
		self.mode()
		self.name()
	
	def mode(self):
		if self.token.code == "IN":
			self.token = self.scanner.GetNextToken()
		if self.token.code == "OUT":
			self.token = self.scanner.GetNextToken()

	def sequenceOfStatements(self):
		self.statement()
		while True:	# should be implemented
			self.statement()


	def statement(self):	# should be implemented
		if self.token.code in (Token.IF, Token.WHILE, Token.LOOP):
			self.compoundStatement()
		else:
			self.simpleStatement()


	def simpleStatement(self):
		if self.token.code == Token.NULL:
			self.nullStatement()
		elif self.token.code == Token.EXIT:
			self.exitStatement()
		else:
			self.nameStatement()	# own method


	def nameStatement(self):
		self.name()


	def compoundStatement(self):
		"ifStatement | loopStatement"
		if self.token.code == Token.IF:
			self.ifStatement()
		else:
			self.loopStatement()


	def nullStatement(self):
		self.accept(Token.NULL, "null expected")
		self.accept(Token.SEMICOLON, "semicolon expected")


	def assignmentStatement(self):
		self.name()	# force <variable>name
		self.accept(Token.COLON_EQ, ":= expected")
		self.expression()
		self.accept(Token.SEMICOLON, "semicolon expected")


	def ifStatement(self):
		self.accept(Token.IF, "if expected")
		self.condition()
		self.accept(Token.THEN, "then expected")
		self.sequenceOfStatements()
		while self.token.code == Token.ELSIF:
			self.token = self.scanner.GetNextToken()
			self.condition()
			self.accept(Token.THEN, "then expected")
			self.sequenceOfStatements()
		if self.token.code == Token.ELSE:
			self.token = self.scanner.GetNextToken()
			self.sequenceOfStatements()
		self.accept(Token.END, "end expected")
		self.accept(Token.IF, "if expected")
		self.accept(Token.SEMICOLON, "semicolon expected")


	def loopStatement(self):
		if self.token.code == Token.WHILE:
			self.iterationScheme()
		self.accept(Token.LOOP, "loop expected")
		self.sequenceOfStatements()
		self.accept(Token.END, "end expected")
		self.accept(Token.LOOP, "loop expected")
		self.accept(Token.SEMICOLON, "semicolon expected")


	def iterationScheme(self):
		self.accept(Token.WHILE, "while expected")
		self.condition()


	def exitStatement(self):
		self.accept(Token.EXIT, "exit expected")
		if self.token.code == Token.WHEN:
			self.condition()
		self.accept(Token.SEMICOLON, "semicolon expected")


	def procedureCallStatement(self):
		self.name() # force <procedure>name
		if self.token.code == Token.PARENTHESIS_OPEN:
			self.actualParameterPart()
		self.accept(Token.SEMICOLON, "semicolon expected")


	def actualParameterPart(self):
		self.accept(Token.PARENTHESIS_OPEN)
		self.expression()
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			self.expression()
		self.accept(Token.PARENTHESIS_CLOSE, "close parenthesis expected")


	def condition(self):
		self.expression() # force <boolean>expression

	
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
		if self.token.code == Token.NOT:
			self.token = self.scanner.GetNextToken()
			self.primary()
		else:
			self.primary()
			if self.token.code == Token.SQUARE:
				self.token = self.scanner.GetNextToken()
				self.primary()


	def primary(self):
		if self.token.code in (Token.numericalLiteral, Token.stringLiteral):
			self.token.GetNextToken
		elif self.token.code == Token.identifier:
			self.name()
		elif self.token.code == "(":
			self.token = self.scanner.GetNextToken()
			self.expression()
			self.accept(Token.PARENTHESIS_CLOSE, "\')\' expected")


	def name(self):
		self.accept(Token.ID)
		if self.token.code == "(":	# indexedComponent
			self.indexedComponent()


	def indexedComponent(self):
		self.accept(Token.PARENTHESIS_OPEN, "\'(\' expected")
		self.expression()
		while self.token.code == Token.COMMA:
			self.accept(Token.COMMA, "\'(\' expected")
			self.expression()
		self.accept(Token.PARENTHESIS_CLOSE, "\')\' expected")


		#모든 메소드를 호출하면 GetNextToken 이 자동으로 됨 
		#따라서 메소드를 호출한 후에는 GetNextToken 사용 금지 
		#함수를 호출하지 않고 종료되거나 다음 토큰을 봐야 할 경우 사용 




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

