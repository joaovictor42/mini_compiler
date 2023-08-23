from lexical.scanner import Scanner
from exceptions import LexicalException, SyntaxException


def main():
	scanner = Scanner("source_code.mc")
	
	while True:
		try:
			token = scanner.next_token()
		except (LexicalException, SyntaxException) as e:
			print(e.message)
			break
		except EOFError:
			print("End of file reached!")
			break
		else:
			print(token)


if __name__ == "__main__":
	main()
