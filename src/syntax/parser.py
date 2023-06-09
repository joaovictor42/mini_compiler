
from lexical.scanner import Scanner
from utils.token_type import TokenType


class Parser:
	def __init__(self, scanner: Scanner) -> None:
		self.scanner = scanner
		self.token = None

	def programa(self) -> None:
		self.token = self.scanner.next_token()
		if not self._match_token(':'):
			message = f"'ROTULO ':' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)

		self.token = self.scanner.next_token()
		if not self._match_token('DECLARACOES'):
			message = f"ROTULO 'DECLARACOES' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		self._listaDeclaracoes()

		if not self._match_token(':'):
			message = f"':' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		if not self._match_token('ALGORITMO'):
			message = f"ROTULO 'ALGORITMO' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		self._listaComandos()

	def _listaDeclaracoes(self) -> None:
		if self._match_token(':'):
			return

		self._varLista()
		if not self._match_token(':'):
			message = f"':' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		self._tipoVar()

		self.token = self.scanner.next_token()
		if not self._match_token(';'):
			message = f"';' expected\n"
			message += f"Line: {self.scanner.line - 1} Column: {self.scanner.column}"
			raise SyntaxError(message)

		self.token = self.scanner.next_token()
		self._listaDeclaracoes()


	def _varLista(self) -> None:
		if not self._match_type(TokenType.VARIAVEL):
			message = f"TIPO 'VARIAVEL' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		if self._match_token(','):
			self.token = self.scanner.next_token()
			self._varLista()
		return

	def _tipoVar(self) -> None:
		if not self._match_token('INTEIRO') and not self._match_token('REAL'):
			message = f"T	ed\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
	
	def _expressaoAritmetica(self) -> None:
		self._termoAritmetico()
		self._expressaoAritmetica2()

	def _expressaoAritmetica2(self) -> None:
		if self._match_token('+') or self._match_token('-'):
			self.token = self.scanner.next_token()
			self._termoAritmetico()
			self._expressaoAritmetica2()
		else:
			return

	def _termoAritmetico(self) -> None:
		self._fatorAritmetico()
		self._termoAritmetico2()

	def _termoAritmetico2(self) -> None:
		if self._match_token('*') or self._match_token('/'):
			self.token = self.scanner.next_token()
			self._fatorAritmetico()
			self._termoAritmetico2()
		else:
			return

	def _termoAritmetico3(self) -> None:
		if not self._match_token('*') and not self._match_token('/'):
			message = f"'*' or '/' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		self._fatorAritmetico()

	def _fatorAritmetico(self) -> None:
		if self._match_type(TokenType.VARIAVEL):
			pass
		elif self._match_type(TokenType.INTEIRO):
			pass
		elif self._match_type(TokenType.REAL):
			pass
		elif self._match_token('('):
			self.token = self.scanner.next_token()
			self._expressaoAritmetica()
			if not self._match_token(')'):
				message = f"')' expected\n"
				message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
				raise SyntaxError(message)
		else:
			message = f"'TIPO' VARIAVEL, INTEIRO, REAL or '(' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()


	def _listaComandos(self) -> None:		
		self._comando()

		self.token = self.scanner.next_token()
		if self.token.content not in ['ASSIGN', 'INPUT', 'PRINT', 'IF', 'WHILE']:
			return 
		self._listaComandos()

	def _comando(self) -> None:
		if self._match_token('ASSIGN'): # OK
			self._comandoAtribuicao()
		elif self._match_token('INPUT'): # OK
			self._comandoEntrada()
		elif self._match_token('PRINT'): # OK
			self._comandoSaida()
		elif self._match_token('IF'):
			self._comandoCondicao()
		elif self._match_token('WHILE'):
			self._comandoRepeticao()
		else:
			message = f"COMMANDO expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		

	def _comandoAtribuicao(self) -> None:
		self.token = self.scanner.next_token()
		self._expressaoAritmetica()
		if not self._match_token('TO'):
			message = f"'TO' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		if not self._match_type(TokenType.VARIAVEL):
			message = f"TIPO 'VARIAVEL' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		if not self._match_token(';'):
			message = f"';' expected\n"
			message += f"Line: {self.scanner.line -1} Column: {self.scanner.column}"
			raise SyntaxError(message)

		
	def _comandoEntrada(self) -> None:
		self.token = self.scanner.next_token()
		if not self._match_type(TokenType.VARIAVEL):
			message = f"TIPO 'VARIAVEL' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		if not self._match_token(';'):
			message = f"';' expected\n"
			message += f"Line: {self.scanner.line -1} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		
	def _comandoSaida(self) -> None:
		self.token = self.scanner.next_token()
		if not self._match_token('('):
			message = f"'(' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		if (not self._match_type(TokenType.VARIAVEL) and not self._match_type(TokenType.CADEIA) 
			and not self._match_type(TokenType.INTEIRO) and not self._match_type(TokenType.REAL)):
			message = f"TIPO 'VARIAVEL', 'CADEIA', 'INTEIRO' or 'REAL' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		if not self._match_token(')'):
			message = f"')' expected"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
		self.token = self.scanner.next_token()
		if not self._match_token(';'):
			message = f"';' expected\n"
			message += f"Line: {self.scanner.line -1} Column: {self.scanner.column}"
			raise SyntaxError(message)
		
	def _comandoCondicao(self) -> None:
		self.token = self.scanner.next_token()
		self._expressaoRelacional()
		if not self._match_token('THEN'):
			message = f"'THEN' expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		self._listaComandos()
		self.token = self.scanner.next_token()
		self._comandoCondicao2()

	def _comandoCondicao2(self) -> None:
		if self._match_token('ELSE'):
			self.token = self.scanner.next_token()
			self._listaComandos()
		else:
			return
		
	def _expressaoRelacional(self) -> None:
		self._termoRelacional()
		self._expressaoRelacional2()

	def _expressaoRelacional2(self) -> None:
		if self._match_type(TokenType.RELATIONAL_OPERATOR):
			self.token = self.scanner.next_token()
			self._termoRelacional()
			self._expressaoRelacional2()
		else:
			return
		
	def _termoRelacional(self) -> None:
		if self._match_token('('):
			self.token = self.scanner.next_token()
			self._expressaoRelacional()
			if not self._match_token(')'):
				message = f"')' expected\n"
				message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
				raise SyntaxError(message)
		else: 
			self._expressaoAritmetica()
			self._operadorRelacional()
			self._expressaoAritmetica()
	

	def _operadorRelacional(self) -> None:
		if not self._match_type(TokenType.RELATIONAL_OPERATOR):
			message = f"Relational Operator expected\n"
			message += f"Line: {self.scanner.line} Column: {self.scanner.column}"
			raise SyntaxError(message)
		self.token = self.scanner.next_token()
		
	def _comandoRepeticao(self) -> None:
		self.token = self.scanner.next_token()
		self._expressaoRelacional()
		self._listaComandos()

	def _match_token(self, token: str) -> bool:
		return self.token.content == token

	def _match_type(self, type: TokenType) -> bool:
		return self.token.type == type