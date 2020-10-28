from Const import Const
from Token import Token
from Chario import Chario


class Scanner:
	"""
	The Scanner class recognizes and generates tokens
	in a stream of characters and returns these tokens to the parser.
	The Scanner class also detects any lexical errors.
	"""
	def __init__(self, chario):
		self.chario = chario


	def StringToken(self):
		"""
		Scans a string literal surrounded by \", e.g. "hahahoho"
		"""
		# remove first \"
		self.chario.GetNextChar()

		result = ""
		while self.chario.PeekNextChar() != "\"":
			result += self.chario.GetNextChar()

		# remove last \"
		self.chario.GetNextChar()
		return Token(Const.stringLiteral, result)


	def IntegerToken(self):
		"""
		Scans an integer value, which is a series of digits
		"""
		result = ""
		while self.chario.PeekNextChar().isdigit():
			result += self.chario.GetNextChar()

		return Token(Const.numericalLiteral, result)


	def AlphabeticToken(self):
		"""
		Scans either an identifier(e.g. variable name) or a reserved word(e.g. is, null).
		"""
		# list of characters that cannot exist right after an identifier or a reserved word
		delimiters = (" ", "\n", "\r", "\t", "\\", ",", ":", "<", ">", "=", ";", "+", "-", "*", "/", "(", ")", "EOF")

		# scan the token
		result = ""
		while self.chario.PeekNextChar() not in delimiters:
			result += self.chario.GetNextChar()

		# return the result as either reserved word itself or an identifier
		if result in Const.reservedWords:
			return Token(result, None)
		else:
			return Token(Const.ID, result)


	def OperatorToken(self):
		"""
		Scans an operator symbol from chario(e.g. +, :=).
		If an unexpected character is detected, RuntimeError will be raised.
		"""
		singleCharOperators = ("+", "-", ";", "(", ")", ",", "=")
		possiblyDoubleCharOperators = ("/", ":", ">", "<", "*")
		doubleCharOperators = ("/=", ":=", "<=", ">=", "**")

		# look for ".." first
		firstChar = self.chario.GetNextChar()
		if firstChar == "." and self.chario.PeekNextChar() == ".":
			self.chario.GetNextChar()
			return Token(Const.DOT_DOT, None)

		# then look for definitely single character operators(e.g. +)
		if firstChar in singleCharOperators:
			return Token(firstChar, None)
		else:
			# if not, check if the character is possibly a double character operator
			# (which is also a valid one by itself, e.g. *)
			if firstChar in possiblyDoubleCharOperators:
				candidate = firstChar + self.chario.PeekNextChar()
				# check if the next character also contributes on making a double character operator(e.g. **)
				if candidate in doubleCharOperators:
					return Token(firstChar + self.chario.GetNextChar(), None)
				else:
					return Token(firstChar, None)
			# if none of the above were the case, then its a unexpected symbol
			else:
				self.chario.PrintErrorMessage("Unexpected symbol '" + firstChar + "' was scanned")
				return Token(Const.UET, firstChar)


	def GetNextToken(self):
		"""
		Read characters from chario and return the first token found
		"""
		# remove ignored characters
		ignoredCharacters = (" ", "\r", "\t")
		while True:
			nextChar = self.chario.PeekNextChar()
			if nextChar == "EOF":
				return Token(Const.EOF, None)

			if nextChar in ignoredCharacters:
				self.chario.GetNextChar()
			else:
				break

		# check the type of this token.
		# this scanner assumes that all identifiers start with an alphabet.
		nextChar = self.chario.PeekNextChar()
		if nextChar == Const.NEWLINE:
			self.chario.GetNextChar()
			return Token(Const.NEWLINE, None)
		elif nextChar == "\"":
			return self.StringToken()
		elif nextChar.isalpha():
			return self.AlphabeticToken()
		elif nextChar.isdigit():
			return self.IntegerToken()
		else:
			return self.OperatorToken()
