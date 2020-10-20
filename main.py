from Token import Token
from Chario import Chario
from Scanner import Scanner
from Parser import Parser


if __name__ == "__main__":
	# FILE_NAME = input("Input the file name: ")	# submission code
	FILE_NAME = "./sample_input/sample_edit.ada"	# DEV code
	chario = Chario(FILE_NAME)	# link the input source file
	scanner = Scanner(chario)
	parser = Parser(chario, scanner)
	# do syntax analysis
	parser.subprogramBody()
	# print("DONE")
	
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

