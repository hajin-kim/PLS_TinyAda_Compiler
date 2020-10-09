import pandas as pd


scannerUnit = pd.Series({
	"BLANK": " ",
	"COMMA":  ",",
	"COLON":  ":",
	"SEMICOLON":  ";",
	"DOT_DOT":  "..",
	"PARENTHESIS_OPEN":  "(",
	"PARENTHESIS_CLOSE":  ")",
	"COLON_EQ":  ":="
})

reserved = pd.Series({
	"IS": "is",
	"BEGIN":  "begin",
	"END":  "end",
	"RANGE_SPACE":  "range ",
	"ARRAY":  "array",
	"OF":  "of",
	"IN":  "in",
	"OUT":  "out",
	"THEN":  "then",
	"ELSIF":  "elsif",
	"ELSE":  "else",
	"WHEN":  "when"
})

basicDeclarationHandles = pd.Series({
	"TYPE":  "type",
	"ID": "id",		# page 249
	"PROC":  "procedure",
})

statementHandles = pd.Series({
	"EXIT":  "exit",
	"ID": "id",		# page 249
	"IF":  "if",
	"LOOP":  "loop",
	"NULL": "null",		# page 249
	"WHILE":  "while",
})

addingOperator = pd.Series({
	"PLUS": "+",
	"MINUS":  "-"
})

multiplyingOperator = pd.Series({
	"MUL": "*",
	"DIV":  "/",
	"MOD":  "mod"
})

powerOperator = pd.Series({
	"SQUARE": "**",
})

relationalOperator = pd.Series({
	"EQ": "=" ,
	"NE":  "/=" ,
	"LT":  "<" ,
	"LE":  "<=" ,
	"GT":  ">" ,
	"GE":  ">="
})

