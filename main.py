from consts import *	# should be copied

from Token import Token
from Chario import Chario
from Scanner import Scanner
from Parser import Parser


if __name__ == "__main__":
	chario = Chario("sample_edit.ada")
	scanner = Scanner(chario)
	parser = Parser(chario, scanner)
	parser.subprogramBody()
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

	# while True:
	# 	token = scanner.GetNextToken()
	# 	if token.value is not None:
	# 		print("token: " + token.code + " value: " + token.value)
	# 	else:
	# 		print("token: " + token.code)
	# 	if token.code == "EOF":
	# 		break

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

