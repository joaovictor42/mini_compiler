from lexical.scanner import Scanner
from syntax.parser import Parser
from exceptions import LexicalException, SyntaxException


def main():
	try: 
		scanner = Scanner("codigo_fonte_que_deve_rodar_apos_a_implementacao.mc")
		parser = Parser(scanner)
		parser.programa()
		print("Compilation successful!")
	except (LexicalException, SyntaxException) as e:
		print(e.message)
	except EOFError:
		print("End of file reached!")
	
if __name__ == "__main__":
	main()
