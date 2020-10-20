class Const:
	"""
	The Const class contains the reserved codes of the Token class.
	"""
	
	# delimiter
	BLANK =" "
	NEWLINE ="\n"
	TAB ="\t"
	CR = "\r"
	BACKSLASH = "\\"
	COMMA = ","
	COLON = ":"
	SEMICOLON = ";"
	DOT_DOT = ".."
	PARENTHESIS_OPEN = "("
	PARENTHESIS_CLOSE = ")"
	COLON_EQ = ":="

	# reserved words
	IS ="is"
	BEGIN = "begin"
	END = "end"
	RANGE = "range"
	ARRAY = "array"
	OF = "of"
	IN = "in"
	OUT = "out"
	THEN = "then"
	ELSIF = "elsif"
	ELSE = "else"
	WHEN = "when"
	CONSTANT = "constant"
	TYPE = "type"
	PROC = "procedure"
	EXIT = "exit"
	IF = "if"
	LOOP = "loop"
	NULL ="null"		# page 249
	WHILE = "while"

	# operators
	PLUS ="+"
	MINUS ="-"
	MUL ="*"
	DIV = "/"
	SQUARE ="**"
	EQ ="=" 
	NE ="/=" 
	LT ="<" 
	LE ="<=" 
	GT =">" 
	GE =">="
	MOD ="mod"	# note
	NOT ="not"
	AND ="and"
	OR ="or"

	# special codes
	ID = "identifier"
	numericalLiteral = "numericalLiteral"
	stringLiteral = "stringLiteral"
	EOF = "EOF"
	UET = "unexpectedToken"

	basicDeclarationHandles = (ID, PROC, TYPE)
	statementHandles = (EXIT, ID, IF, LOOP, NULL, WHILE)
	relationalOperator = (EQ, NE, LT, LE, GT, GE,)
	addingOperator = (PLUS, MINUS)
	multiplyingOperator = (MUL, DIV, MOD)

	reservedWords = (
		IS, BEGIN, END, RANGE, ARRAY, OF, IN, OUT, 
		THEN, ELSIF, ELSE, WHEN, CONSTANT, 
		TYPE, PROC, 
		EXIT, IF, LOOP, NULL, WHILE, 
		MOD, NOT, AND, OR
	)


# factorOperator = pd.Series({
# 	"SQUARE": "**"
# })
# 

# stringOperator = pd.Series({
# 	"MOD": "mod",	# note
# 	"NOT": "not",
# 	"AND": "and",
# 	"OR": "or"
# })

# scannerUnit = pd.concat((tokenizer, addingOperator, multiplyingOperator, factorOperator, relationalOperator))

# tokenCode = pd.concat((tokenizer, reserved, basicDeclarationHandles, statementHandles, addingOperator, multiplyingOperator, factorOperator, relationalOperator)).unique()

