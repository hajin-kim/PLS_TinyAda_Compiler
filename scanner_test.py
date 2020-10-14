from Token import Token
from Chario import Chario
from Scanner import Scanner

if __name__ == "__main__":
	chario = Chario("./sample_input/test.txt")	# link the input source file
	scanner = Scanner(chario)

	while True:
		token = scanner.GetNextToken()
		if token.value is not None:
			print("token: " + token.code + " value: " + token.value)
		else:
			print("token: " + token.code)
		if token.code == "EOF":
			break
