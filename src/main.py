from lexical.scanner import Scanner
from lexical.exceptions import CompileLexicalError


def main():
	scanner = Scanner("source_code.mc")
	
	while True:
		try:
			token = scanner.next_token()
		except CompileLexicalError as e:
			print("Lexical error: " + e.message)
			break
		except EOFError:
			print("End of file reached!")
			break
		else:
			print(token)


if __name__ == "__main__":
	main()
