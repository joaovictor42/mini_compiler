from utils.token_type import TokenType
from lexical.token import Token
import traceback

class Scanner:
    
	def __init__(self, filename: str) -> None:
		self.pos = 0

		try:
			with open(filename, "r") as file:
				self.content = file.read()
		except Exception as e:
			print("Error while reading file: " + filename)
			traceback.print_exc()
		
	
	def next_token(self) -> Token:
		self.state = 0
		content = ""

		while True:
			if self.is_eof():
				return None
			current_char = self.next_char()

			# START
			if self.state == 0:
				if is_space(current_char):
					continue
				if is_inline_comment(current_char):
					self.state = -1
				# GOT TO IDENTYFIER
				elif is_letter(current_char) or current_char == '_':
					content += current_char
					self.state = 1
				# GOT TO NUMBER
				elif is_digit(current_char):
					content += current_char
					self.state = 2
				# RELATIONAL OPERATOR
				elif is_relational_operator(current_char):
					content += current_char
					self.state = 3
				# ASSIGNMENT
				elif is_assignment_operator(current_char):
					return Token(TokenType.ASSIGNMENT, current_char)
				# ARITHMETIC OPERATOR
				elif is_arithmetic_operator(current_char):
					return Token(TokenType.ARI_OP, current_char)

			# IDENTYFIER
			elif self.state == 1:
				if is_letter(current_char) or current_char == '_' or is_digit(current_char):
					content += current_char
					self.state = 1
				else:
					self.back()
					return Token(TokenType.IDENTYFIER, content)
			
			# NUMBER
			elif self.state == 2:
				if self.is_digit(current_char):
					content += current_char
					self.state = 2
				elif self.is_letter(current_char):
					raise RuntimeError("Number Malformed!")
				else:
					self.back()
					return Token(TokenType.NUMBER, content)
				
			# RELATIONAL OPERATOR
			elif self.state == 3:
				if current_char == '=':
					content += current_char
				else:
					self.back()
				return Token(TokenType.REL_OP, content)
			
			# INLINE COMMENT
			elif self.state == -1:
				if not end_of_line(current_char):
					continue
				self.state = 0
					

	def next_char(self) -> str:
		self.pos += 1
		return self.content[self.pos]

	def back(self) -> None:
		self.pos -= 1

	def is_eof(self) -> bool:
		if self.pos >= len(self.content):
			return True
		return False
	

def is_letter(char: str) -> bool:
	return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')

def is_digit(char: str) -> bool:
	return char >= '0' and char <= '9'

def is_inline_comment(char: str) -> bool:
	return char == '#'

def is_space(char: str) -> bool:
	return char in [' ', '\n', '\t', '\r']
	
def is_relational_operator(char: str) -> bool:
	return char in ['>', '<', '=', '!']

def is_arithmetic_operator(char: str) -> bool:
	return char in ['+', '-', '*', '/']

def is_assignment_operator(char: str) -> bool:
	return char == '='

def end_of_line(char: str) -> bool:
	return char in ['\n', '\r']