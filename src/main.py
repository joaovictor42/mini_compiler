from lexical.scanner import Scanner


def main():
	scanner = Scanner("source_code.mc")
	
	while True:
		token = scanner.next_token()
		print(token)

		if token is None:
			break

if __name__ == "__main__":
	main()
