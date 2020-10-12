from consts import *


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
	EOF = "EOF"
	ID = "id"
	numericalLiteral = "int"
	stringLiteral = "id"
	basicDeclarationHandles = (ID, PROC, TYPE)
	relationalOperator = (EQ, NE, LT, LE, GT, GE,)
	addingOperator = (PLUS, MINUS)
	multiplyingOperator = (MUL, DIV, MOD)

	def __init__(self, code, value):
		self.code = code
		self.value = value



