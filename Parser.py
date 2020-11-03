from Token import Token
from Chario import Chario
from Scanner import Scanner
from SymbolTable import SymbolTable
from SymbolEntry import SymbolEntry


class Parser:
	"""
	The Parser class uses a recursive descent strategy
	to recognize phrases in a stream of tokens. Unlike the scanner,
	which continues to generate tokens after lexical errors,
	the parser halts execution upon encountering
	the first syntax error in a source program.
	"""
	def __init__(self, chario, scanner):
		"""
		construct a Parser instance
		
		Arguments:
			chario -- the instance of Chario
			scanner -- the instance of Scanner
		"""
		self.chario = chario
		self.scanner = scanner
		# should implement handles
		#self.initHandles()
		self.token = scanner.GetNextToken()
		self.table = SymbolTable(self.chario)

		# init SymbolTable
		self.table.enterScope()
		self.table.enterSymbol("BOOLEAN", SymbolEntry.TYPE)
		self.table.enterSymbol("CHAR", SymbolEntry.TYPE)
		self.table.enterSymbol("INTEGER", SymbolEntry.TYPE)
		self.table.enterSymbol("MATRIX", SymbolEntry.TYPE)
		self.table.enterSymbol("PRINT", SymbolEntry.PROC)
		self.table.enterSymbol("TRUE", SymbolEntry.CONST, True)
		self.table.enterSymbol("FALSE", SymbolEntry.CONST, False)


	def parse(self):
		"""
		do parse the entire source code
		"""
		self.subprogramBody()
		# accept EOF: check if extra symbols after logical end of program exist
		#self.accept(Token.EOF)


	def pushSymbols(self, identifierList, role=None, value=None):
		"""
		push identifiers in iterable into the table stack
		
		Arguments:
			identifierList {[iterable]} -- container of identifier name strings
		
		Keyword Arguments:
			role {[str, None]} -- SymbolEntry role constants, optional (default: {None})
		"""
		for identifier in identifierList:
			self.table.enterSymbol(identifier, role, value)


	# def setRole(self, identifierList, role):
	# 	for identifier in identifierList:
	# 		entry = self.table.findSymbol(identifier)
	# 		if entry is None:
	# 			////
	# 		entry.role = role


	def ignore_newlines(self):
		"""
		ignore preceding newlines("\n") and unexpected tokens.
		error message for unexpected token is handled in scanner class.
		"""
		while self.token.code in (Token.NEWLINE, Token.UET):
			self.token = self.scanner.GetNextToken()


	def discard_tokens(self):
			# give up parsing the line with an error by discarding all trailling tokens until a newline character
			message = "trailing tokens: " + str(self.token) + " "
			
			if self.token.code not in (Token.NEWLINE, Token.EOF):
				self.token = self.scanner.GetNextToken()
				while self.token.code not in (Token.NEWLINE, Token.EOF):
					message += str(self.token) + " "
					self.token = self.scanner.GetNextToken()
					
			message += "were discarded"
			
			# prepare next token other than newline for next parsing attempt
			self.ignore_newlines()

			print(message)


	def accept(self, expected, error_message):
		"""
		accept the current token only with the expected code

		Arguments:
			expected {Token.{code}} -- expected token code
			error_message {str} -- error message if unacceptable
		"""
		# prepare error message first
		error_message = "expected [" + expected + "] but " + str(self.token) + " was detected"

		# these tokens always appear that the end of a line
		line_terminating_tokens = (Token.IS, Token.LOOP, Token.SEMICOLON, Token.BEGIN, Token.THEN)

		# if the last token of this line was an unexpected one,
		# do not remove that newline to preserve the next line's tokens
		# (if we do ignore it, all the tokens in the next line will be discarded!)
		if self.token.code == Token.NEWLINE and expected in line_terminating_tokens:
			self.fatalError(error_message)
		
		self.ignore_newlines()

		if self.token.code != expected:

			# raise error!
			self.fatalError(error_message)
		# print("hahahoho")

		self.token = self.scanner.GetNextToken()
		if expected in line_terminating_tokens:
			self.ignore_newlines()


	def acceptRole(self, identifier, expected):
		"""
		accept the identifier is expected
		
		Arguments:
			identifier {str} -- name of the identifier
			expected {str} -- SymbolEntry role constants
		"""
		entry = self.table.findSymbol(identifier)
		if (not entry is None and entry.role != expected):
			if expected == SymbolEntry.VAR and entry.role == SymbolEntry.PARAM:
				return
			self.chario.PrintErrorMessage(entry.name + ": expected " + expected + " identifier, not " + entry.role)


	def fatalError(self, error_message):
		"""
		send error message to the Chario instance and throw RuntimeError

		Arguments:
			error_message {str} -- error message to send to the Chario
		"""
		self.chario.PrintErrorMessage(error_message)
		self.discard_tokens()
		raise RuntimeError("Fatal error: " + error_message)


	def subprogramBody(self):
		"""
		Check whole subprogram matches to EBNF grammar for TinyAda
		"""

		procedure_name = None
		try:
			procedure_name = self.subprogramSpecification()
			self.accept(Token.IS,
						"\'" + Token.IS + "\' expected")
		except RuntimeError as e:
			print("continue parsing from declarative part of subprogram body\n")

		try:
			self.declarativePart()
		except RuntimeError as e:
			print("continue parsing from [begin] of subprogram body\n")

		try:
			self.accept(Token.BEGIN,
						"\'" + Token.BEGIN + "\' expected")
			# print("hahahoho")
		except RuntimeError as e:
			print("continue parsing from sequence of statement of subprogram body\n")

		try:
			self.sequenceOfStatements()
		except RuntimeError as e:
			print("continue parsing from [end] of subprogram body\n")

		try:
			# print("hahahoho")
			self.accept(Token.END,
						"\'" + Token.END + "\' expected")
			self.table.exitScope()

			# force <procedure>identifier
			if self.token.code == Token.ID:
				identifier = self.token.value
				self.acceptRole(identifier, SymbolEntry.PROC)
				if identifier != procedure_name:
					self.chario.PrintErrorMessage("unexpected [" + identifier + "], expected [" + procedure_name + "]")
				self.token = self.scanner.GetNextToken()

			self.accept(Token.SEMICOLON, 
						"semicolon expected")
		except RuntimeError as e:
			# print("hahahoho")

			print("stop parsing subprogram body\n")


	def declarativePart(self):
		"""
		call basicDeclaration function while token is in basicDeclarationHandles
		"""
		while self.token.code in Token.basicDeclarationHandles:
			try:
				self.basicDeclaration()
			except RuntimeError as e:
				print("continue parsing basic declaration of declarative part\n")


	def basicDeclaration(self):
		"""
		check which declaration the token is and call declaration function
		"""
		if self.token.code == Token.ID:
			self.numberOrObjectDeclaration()
		elif self.token.code == Token.TYPE:
			self.typeDeclaration()
		elif self.token.code == Token.PROC:
			self.subprogramBody()


	def numberOrObjectDeclaration(self):
		"""
		as number declaration and Object declaration both have identifierList
		and ":",  this function first parsing identifierList and ":".
		Then check the token is number declaration Or Object declaration 
		and call declaration function
		"""
		identifiers = self.identifierList()
		self.accept(Token.COLON,
					"\'" + Token.COLON + "\' expected")
		if self.token.code == Token.CONSTANT:
			value = self.numberDeclaration()
			self.pushSymbols(identifiers, SymbolEntry.CONST, value)
		else:
			self.objectDeclaration()
			self.pushSymbols(identifiers, SymbolEntry.VAR)


	def objectDeclaration(self):
		"""
		check the statement has typeDefinition and ";"
		"""
		self.typeDefinition()
		self.accept(Token.SEMICOLON,
					"\'" + Token.SEMICOLON + "\' expected")


	def numberDeclaration(self):
		"""
		check the statement has  "constant", ":=", <static>expression and ";"
		"""
		self.accept(Token.CONSTANT,
					"\'" + "constant" + "\' expected")
		self.accept(Token.COLON_EQ,
					"\'" + Token.COLON_EQ + "\' expected")
		value = self.expression()	# TODO: force <static>expression
		self.accept(Token.SEMICOLON,
					"\'" + Token.SEMICOLON + "\' expected")

		return value


	def identifierList(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		identifierList = identifier { "," identifier }
		"""
		identifiers = []

		identifiers.append(self.token.value)
		self.accept(Token.ID,
					"identifier expected")
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			identifiers.append(self.token.value)
			self.accept(Token.ID,
						"identifier expected")

		return identifiers


	def typeDeclaration(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		typeDeclaration = "type" identifier "is" typeDefinition ";"
		"""
		self.accept(Token.TYPE,
					"\'" + Token.TYPE + "\' expected")
		identifier = self.token.value
		self.accept(Token.ID,
					"identifier expected")
		self.accept(Token.IS,
					"\'" + Token.IS + "\' expected")
		self.typeDefinition()
		self.accept(Token.SEMICOLON,
					"\'" + Token.SEMICOLON + "\' expected")
		self.table.enterSymbol(identifier, SymbolEntry.TYPE)


	def typeDefinition(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		typeDefinition = enumerationTypeDefinition | arrayTypeDefinition
 		| range | <type>name
		"""
		if self.token.code == Token.PARENTHESIS_OPEN:
			self.enumerationTypeDefinition()
		elif self.token.code == Token.ARRAY:
			self.arrayTypeDefinition()
		elif self.token.code == Token.RANGE:
			self.range()
		elif self.token.code == Token.ID:
			# force <type>name
			# self.acceptRole(self.token.value, SymbolEntry.TYPE)
			entry = self.name()
			if entry != None and entry.role != SymbolEntry.TYPE:
				self.chario.PrintErrorMessage(entry.name + ": expected " + SymbolEntry.TYPE + " identifier, not " + entry.role)
		else:
			self.fatalError("expected either an opening parenthesis, an array,"+\
			" a range, or an identifier but " + str(self.token) + " was detected")


	def range(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		range = "range " simpleExpression ".." simpleExpression
		"""
		self.accept(Token.RANGE,
					"\'" + Token.IS + "\' expected")
		# print(" T: entering")
		self.simpleExpression()
		# print(" T: breaking")
		self.accept(Token.DOT_DOT,
					"\'" + Token.DOT_DOT + "\' expected")
		self.simpleExpression()
		# print(" T: escaping")



	def index(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		index = range | <type>name
		"""
		if self.token.code == Token.RANGE:
			self.range()
		elif self.token.code == Token.ID:
			# force <type>name
			# self.acceptRole(self.token.value, SymbolEntry.TYPE)
			entry = self.name()
			if entry != None and entry.role != SymbolEntry.TYPE:
				self.chario.PrintErrorMessage(entry.name + ": expected " + SymbolEntry.TYPE + " identifier, not " + entry.role)
		else:
			self.fatalError("error in indexing")


	def enumerationTypeDefinition(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		enumerationTypeDefinition = "(" identifierList ")"
		"""
		self.accept(Token.PARENTHESIS_OPEN,
					"\'" + Token.PARENTHESIS_OPEN + "\' expected")
		identifiers = self.identifierList()
		self.accept(Token.PARENTHESIS_CLOSE,
					"\'" + Token.PARENTHESIS_CLOSE + "\' expected")
		self.table.pushSymbols(identifiers, SymbolEntry.CONST)


	def arrayTypeDefinition(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		arrayTypeDefinition = "array" "(" index { "," index } ")" "of" <type>name
		"""
		self.accept(Token.ARRAY,
					"\'" + Token.ARRAY + "\' expected")
		self.accept(Token.PARENTHESIS_OPEN,
					"\'" + Token.PARENTHESIS_OPEN + "\' expected")
		self.index()
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			self.index()
		self.accept(Token.PARENTHESIS_CLOSE,
					"\'" + Token.PARENTHESIS_CLOSE + "\' expected")
		self.accept(Token.OF,
					"\'" + Token.OF + "\' expected")
		# force <type>name
		# self.acceptRole(self.token.value, SymbolEntry.TYPE)
		entry = self.name()
		if entry != None and entry.role != SymbolEntry.TYPE:
			self.chario.PrintErrorMessage(entry.name + ": expected " + SymbolEntry.TYPE + " identifier, not " + entry.role)


	def subprogramSpecification(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		subprogramSpecification = "procedure" identifier [ formalPart ]
		"""
		self.accept(Token.PROC,
					"procedure expected")
		identifier = self.token.value
		self.accept(Token.ID,
					"identifier expected")	# TODO: enter symbol of procedure identifier
		self.table.enterSymbol(identifier, SymbolEntry.PROC)
		self.table.enterScope()	# TODO
		if self.token.code == "(":	# TODO: note
			self.formalPart()
		return identifier


	def formalPart(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		formalPart = "(" parameterSpecification { ";" parameterSpecification } ")"
		"""
		self.accept(Token.PARENTHESIS_OPEN,
					"\'" + Token.PARENTHESIS_OPEN + "\' expected")
		self.parameterSpecification()
		while self.token.code == Token.SEMICOLON:
			self.token = self.scanner.GetNextToken()
			self.parameterSpecification()
		self.accept(Token.PARENTHESIS_CLOSE,
					"\'" + Token.PARENTHESIS_CLOSE + "\' expected")


	def parameterSpecification(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		parameterSpecification = identifierList ":" mode <type>name
		"""
		identifiers = self.identifierList()
		self.accept(Token.COLON,
					"\'" + Token.COLON + "\' expected")
		self.mode()
		# force <type>name
		# self.acceptRole(self.token.value, SymbolEntry.TYPE)
		entry = self.name()
		if entry != None and entry.role != SymbolEntry.TYPE:
			self.chario.PrintErrorMessage(entry.name + ": expected " + SymbolEntry.TYPE + " identifier, not " + entry.role)
		self.pushSymbols(identifiers, SymbolEntry.PARAM)


	def mode(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		mode = [ "in" ] | "in" "out" | "out"
		"""
		if self.token.code == Token.IN:
			self.token = self.scanner.GetNextToken()
		if self.token.code == Token.OUT:
			self.token = self.scanner.GetNextToken()


	def sequenceOfStatements(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		sequenceOfStatements = statement { statement }
		"""
		self.statement()
		while self.token.code not in (Token.END, Token.ELSIF, Token.ELSE, Token.EOF):	# TODO: should be implemented -> done
			self.statement()


	def statement(self):	# TODO: should be implemented
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		statement = simpleStatement | compoundStatement
		"""
		try:
			if self.token.code in (Token.IF, Token.WHILE, Token.LOOP):
				self.compoundStatement()
			else:
				self.simpleStatement()
		except:
			print("continue parsing next statement\n")


	def simpleStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		simpleStatement = nullStatement | assignmentStatement
				 | procedureCallStatement | exitStatement
		"""
		if self.token.code == Token.NULL:
			self.nullStatement()
		elif self.token.code == Token.EXIT:
			self.exitStatement()
		else:
			self.nameStatement()	# TODO: resolve comment: own method


	def nameStatement(self):
		"""
		as number procedureCallStatement and assignmentStatement both have name,
		this function first parsing name. Then check the token is assignmentStatement
		or procedureCallStatement and call declaration function
		"""
		identifier = self.token.value
		self.name()
		if self.token.code == Token.COLON_EQ:
			# to invoke assignmentStatement(), force <variable>name
			self.acceptRole(identifier, SymbolEntry.VAR)
			self.table.findSymbol(identifier).value = self.assignmentStatement()
		elif identifier == "print":
			# self.token = self.scanner.GetNextToken()
			self.printProcedureCallStatement()
		else:
			# to invoke procedureStatement(), force <procedure>name
			self.acceptRole(identifier, SymbolEntry.PROC)
			self.procedureCallStatement()


	def compoundStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		compoundStatement = ifStatement | loopStatement
		"""
		if self.token.code == Token.IF:
			self.ifStatement()
		else:
			self.loopStatement()


	def nullStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		nullStatement = "null" ";"
		"""
		self.accept(Token.NULL,
					"null expected")
		self.accept(Token.SEMICOLON,
					"semicolon expected")


	def assignmentStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		assignmentStatement = <variable>name ":=" expression ";"
		"""
		self.accept(Token.COLON_EQ,
					":= expected")
		ret = self.expression()
		self.accept(Token.SEMICOLON,
					"semicolon expected")
		return ret


	def ifStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		ifStatement =
				"if" condition "then" sequenceOfStatements
 				{ "elsif" condition "then" sequenceOfStatements }
 				[ "else" sequenceOfStatements ]
				 "end" "if" ";"
		"""
		self.accept(Token.IF,
					"if expected")
		self.condition()
		self.accept(Token.THEN,
					"then expected")
		self.sequenceOfStatements()
		while self.token.code == Token.ELSIF:
			self.token = self.scanner.GetNextToken()
			self.condition()
			self.accept(Token.THEN,
						"then expected")
			self.sequenceOfStatements()
		if self.token.code == Token.ELSE:
			self.token = self.scanner.GetNextToken()
			self.sequenceOfStatements()
		self.accept(Token.END,
					"end expected")
		self.accept(Token.IF,
					"if expected")
		self.accept(Token.SEMICOLON,
					"semicolon expected")


	def loopStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		loopStatement =
 				[ iterationScheme ] "loop" sequenceOfStatements "end" "loop" ";"
		"""
		try:
			if self.token.code == Token.WHILE:
				self.iterationScheme()
			self.accept(Token.LOOP,
						"loop expected")
		except RuntimeError as e:
			print("continue parsing from sequence of statements of loop statement\n")

		self.sequenceOfStatements()

		try:
			self.accept(Token.END,
						"end expected")
			self.accept(Token.LOOP,
						"loop expected")
			self.accept(Token.SEMICOLON,
						"semicolon expected")
		except RuntimeError as e:
			print("stop parsing loop statement\n")


	def iterationScheme(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		iterationScheme = "while" condition
		"""
		self.accept(Token.WHILE,
					"while expected")
		self.condition()


	def exitStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		exitStatement = "exit" [ "when" condition ] ";"
		"""
		self.accept(Token.EXIT,
					"exit expected")
		if self.token.code == Token.WHEN:
			self.token = self.scanner.GetNextToken()
			self.condition()
		self.accept(Token.SEMICOLON,
					"semicolon expected")


	def procedureCallStatement(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		procedureCallStatement = <procedure>name [ actualParameterPart ] ";"
		"""
		if self.token.code == Token.PARENTHESIS_OPEN:
			self.actualParameterPart()
		self.accept(Token.SEMICOLON,
					"semicolon expected")


	def printProcedureCallStatement(self):
		# print("call print")
		if self.token.code == Token.PARENTHESIS_OPEN:
			# print("ongoing")
			params = self.actualParameterPart()
			for param in params:
				# if param.__class__ == SymbolEntry.__class__:
				# 	print(SymbolEntry.value, end=' ')
				# else:
					print(param, end=' ')
		print()
		self.accept(Token.SEMICOLON,
					"semicolon expected")


	def actualParameterPart(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		actualParameterPart = "(" expression { "," expression } ")"
		"""
		self.accept(Token.PARENTHESIS_OPEN,
					"open parenthesis expected")
		ret = []
		# input("t")
		ret.append(self.expression())
		# input("t")
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			ret.append(self.expression())
		self.accept(Token.PARENTHESIS_CLOSE,
					"close parenthesis expected")
		return ret


	def condition(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		condition = <boolean>expression
		"""
		self.expression() # TODO: force <boolean>expression


	def expression(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		expression = relation { "and" relation } | { "or" relation }
		"""
		value = self.relation()
		if self.token.code == Token.AND:
			while self.token.code == Token.AND:
				self.token = self.scanner.GetNextToken()
				value = value and self.relation()
		elif self.token.code == Token.OR:
			while self.token.code == Token.OR:
				self.token = self.scanner.GetNextToken()
				value = value or self.relation()

		# print(" T: expr result", value)
		return value


	def relation(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		relation = simpleExpression [ relationalOperator simpleExpression ]
		"""
		value = self.simpleExpression()
		if self.token.code in Token.relationalOperator:
			operation = self.token.code

			self.token = self.scanner.GetNextToken()
			operand = self.simpleExpression()
			# TODO: handle relational operation between value and operand

		return value


	def simpleExpression(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		simpleExpression =
				[ unaryAddingOperator ] term { binaryAddingOperator term }
		"""
		sign = None
		if self.token.code in Token.addingOperator:
			if self.token.code == Token.PLUS:
				sign = 1
			else:
				sign = -1
			self.token = self.scanner.GetNextToken()
		value = self.term()
		if sign != None and value != None:
			value = value * sign
		while self.token.code in Token.addingOperator:
			# print("call addition")
			operation = self.token.code

			self.token = self.scanner.GetNextToken()
			operand = self.term()
			if operand == None or value == None:
				value = None
				continue
			if operation == Token.PLUS:
				value = value + operand
			else:
				value = value - operand

		return value


	def term(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		term = factor { multiplyingOperator factor }
		"""
		value = self.factor()
		while self.token.code in Token.multiplyingOperator:
			operation = self.token.code

			self.token = self.scanner.GetNextToken()
			operand = self.factor()
			if operand == None or value == None:
				value = None
				continue
			if operation == Token.MUL:
				value = value * operand
			elif operation == Token.DIV:
				value = value // operand
			else:
				value = value % operand
		
		return value


	def factor(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		factor = primary [ "**" primary ] | "not" primary
		"""
		# not
		value = None
		if self.token.code == Token.NOT:
			self.token = self.scanner.GetNextToken()
			value = self.primary()
			if value != None:
				value = not value
		else:
			value = self.primary()
			if self.token.code == Token.SQUARE:
				self.token = self.scanner.GetNextToken()
				operand = self.primary()
				if operand == None or value == None:
					value = None
				else:
					value = value ** operand

		return value


	def primary(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		primary = numericLiteral | stringLiteral | name | "(" expression ")"
		"""
		value = None
		if self.token.code in (Token.numericalLiteral, Token.stringLiteral):
			value = self.token.value
			if self.token.code is Token.numericalLiteral:
				value = int(value)
			self.token = self.scanner.GetNextToken()
			# print(" T: literal", value)
		elif self.token.code == Token.ID:
			# print(self.token.value, "open")
			entry = self.name()
			# print(self.token.value, "close")

			if entry != None:
				value = entry.value
				# print(" T: identifier", value)
			
		elif self.token.code == Token.PARENTHESIS_OPEN:
			self.token = self.scanner.GetNextToken()
			value = self.expression()
			self.accept(Token.PARENTHESIS_CLOSE,
						"\')\' expected")
		else:
			self.fatalError("expected either a numeric literal, an identifier, or an opening parenthesis but " + 
				str(self.token) + " was detected")

		return value


	def name(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		name = identifier [ indexedComponent ]
		"""
		entry = self.table.findSymbol(self.token.value)
		# print("running name")
		self.accept(Token.ID,
					"identifier expected")
		if (entry == None or entry.role != SymbolEntry.PROC) and self.token.code == Token.PARENTHESIS_OPEN:	# TODO: resolve comment: indexedComponent
			# print("running indexedComponent")
			self.indexedComponent()
		return entry


	def indexedComponent(self):
		"""
		check the statement is in the same format as the EBNF of Tinyada,
		
		indexedComponent = "(" expression { "," expression } ")"
		"""
		self.accept(Token.PARENTHESIS_OPEN,
					"\'(\' expected")
		self.expression()
		while self.token.code == Token.COMMA:
			self.token = self.scanner.GetNextToken()
			self.expression()
		self.accept(Token.PARENTHESIS_CLOSE,
					"\')\' expected")

		# TODO: resolve the following comment
		#모든 메소드를 호출하면 GetNextToken 이 자동으로 됨
		#따라서 메소드를 호출한 후에는 GetNextToken 사용 금지
		#함수를 호출하지 않고 종료되거나 다음 토큰을 봐야 할 경우 사용

