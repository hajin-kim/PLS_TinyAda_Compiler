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

		return Token(Const.numericalLiteral, result)

	def AlphabeticToken(self):
		"""
		Scans either an identifier(e.g. variable name) or a reserved word(e.g. is, null).
		"""
		# print("scanning an alphabetic token...")
		# all possible alphabetic keywords(e.g. is, null, mod)

		# list of characters that cannot exist right after an identifier or a reserved word
		delimiters = (" ", "\n", "\r", "\t", "\\", ",", ":", "<", ">", "=", ";", "+", "-", "*", "/", "(", ")", "EOF")

		# scan the token
		result = ""
		while self.chario.PeekNextChar() not in delimiters:
			# print(self.chario.PeekNextChar() + " was not a delimiter")
			result += self.chario.GetNextChar()

		# print(self.chario.PeekNextChar() + " was a delimiter!")

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
		# print("scanning an operator token...")

		singleCharOperators = ("+", "-", ";", "(", ")", ",", "=")
		possiblyDoubleCharOperators = ("/", ":", ">", "<", "*")
		doubleCharOperators = ("/=", ":=", "<=", ">=", "**")

		# look for .. first
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
				self.chario.PrintErrorMessage("Unexpected symbol '" + firstChar + "'")
				raise RuntimeError("Unexpected symbol")


	def GetNextToken(self):
		"""
		Read characters from chario and return the first token found
		"""
		# print("scanning a token...")
		# remove space and newline
		ignoredCharacters = (" ", "\r", "\t")
		while True:
			nextChar = self.chario.PeekNextChar()
			# print("should I remove "+ nextChar+"?")
			if nextChar == "EOF":
				return Token(Const.EOF, None)

			if nextChar in ignoredCharacters:
				self.chario.GetNextChar()
			else:
				break

		nextChar = self.chario.PeekNextChar()
		if nextChar == Const.NEWLINE:
			self.chario.GetNextChar()
			return Token(Const.NEWLINE, None)
		elif nextChar.isalpha():
			return self.AlphabeticToken()
		elif nextChar.isdigit():
			return self.IntegerToken()
		else:
			return self.OperatorToken()
