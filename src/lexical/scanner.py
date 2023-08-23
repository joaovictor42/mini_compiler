from utils.token_type import TokenType
from utils.reserved_keywords import RESERVED_KEYWORDS
from lexical.token import Token
from exceptions import LexicalException, LexicalError
import traceback

class Scanner:
    
	def __init__(self, filename: str) -> None:
		self.pos = -1
		self.line = 1
		self.column = 0

		try:
			with open(filename, "r") as file:
				self.content = file.read() + '\n'
		except Exception as e:
			print("Error while reading file: " + filename)
			traceback.print_exc()
			exit()
		
	
	def next_token(self) -> Token:
		self.state = 0
		content = ""

		while True:
			if self.is_eof():
				raise EOFError("End of file reached!")
			current_char = self.next_char()

			# START
			if self.state == 0:
				# Skip spaces
				if is_space(current_char):
					continue

				# Go to new line
				elif end_of_line(current_char):
					self.line += 1
					self.column = 0
					continue

				# Inline comment
				elif is_inline_comment(current_char):
					self.state = -1

				# Indentifier
				elif is_letter(current_char) or current_char == '_':
					content += current_char
					self.state = 1

				# Number: prefix is a digit
				elif is_digit(current_char):
					content += current_char
					# Go check suffix
					self.state = 2

				# Number: prefix is a dot
				elif current_char == '.':
					content += current_char
					# Go check suffix
					self.state = 3

				# Relational operator and assignment
				elif is_relational_operator(current_char):
					content += current_char
					self.state = 4
				
				# Arithmetic operator
				elif is_arithmetic_operator(current_char):
					return Token(TokenType.ARITHMETIC_OPERATOR, current_char)
				
				# Open parenthesis
				elif open_parenthesis(current_char):
					return Token(TokenType.LEFT_PARENTHESIS, current_char)
				
				# Close parenthesis
				elif close_parenthesis(current_char):
					return Token(TokenType.RIGHT_PARENTHESIS, current_char)
				
				# Invalid character
				else:
					message = f"{LexicalError.INVALID_CHARACTER}\n"
					message += f"Line: {self.line} Column: {self.column}"
					raise LexicalException(message)
				
			# Inline comment
			elif self.state == -1:
				if not end_of_line(current_char):
					continue
				self.state = 0
				self.line += 1
				self.column = 0
				continue

			# Identifier
			elif self.state == 1:
				if is_letter(current_char) or current_char == '_' or is_digit(current_char):
					content += current_char
				elif (
					is_arithmetic_operator(current_char) or 
					is_relational_operator(current_char) or 
					open_parenthesis(current_char) or
					close_parenthesis(current_char) or
					is_space(current_char) or 
					is_inline_comment(current_char) or
					end_of_line(current_char)
				):
					self.back()
					if content in RESERVED_KEYWORDS:
						return Token(TokenType.RESERVED, content)
					return Token(TokenType.IDENTYFIER, content)
				else:
					message = f"{LexicalError.INDENTIFIER_MALFORMED}\n"
					message += f"Line: {self.line} Column: {self.column}"
					raise LexicalException(message)		
			# number: suffix is a digit or a dot
			elif self.state == 2:
				if is_digit(current_char):
					content += current_char
				# Go to suffix: number
				elif current_char == '.':
					content += current_char
					self.state = 3
				elif (
					is_arithmetic_operator(current_char) or 
					is_relational_operator(current_char) or 
					close_parenthesis(current_char) or
					is_space(current_char) or 
					is_inline_comment(current_char) or
					end_of_line(current_char)
				):
					self.back()
					return Token(TokenType.NUMBER, content)
				else:
					message = f"{LexicalError.NUMBER_MALFORMED}\n"
					message += f"Line: {self.line} Column: {self.column}"
					raise LexicalException(message)
				
			# number: suffix is digit
			elif self.state == 3:
				if is_digit(current_char):
					content += current_char
				elif (
					is_arithmetic_operator(current_char) or 
					is_relational_operator(current_char) or 
					close_parenthesis(current_char) or
					is_space(current_char) or 
					is_inline_comment(current_char) or
					end_of_line(current_char)
				):
					self.back()
					# Check if number ends with dot. Example: 1.
					if content[-1] == ".":
						message = f"{LexicalError.NUMBER_MALFORMED}\n"
						message += f"Line: {self.line} Column: {self.column}"
						raise LexicalException(message)
					return Token(TokenType.NUMBER, content)
				else: 
					message = f"{LexicalError.NUMBER_MALFORMED}\n"
					message += f"Line: {self.line} Column: {self.column}"
					raise LexicalException(message)
			
			# Relational operator and assignment
			elif self.state == 4:
				if current_char == '=':
					content += current_char
					return Token(TokenType.RELATIONAL_OPERATOR, content)
				else:
					self.back()
					if content == '=':
						return Token(TokenType.ASSIGNMENT, content)
					elif content == '!':
						message = f"{LexicalError.RELATIONAL_OPERATOR_MALFORMED}\n"
						message += f"Line: {self.line} Column: {self.column}"
						raise LexicalException(message)
					return Token(TokenType.RELATIONAL_OPERATOR, content)
					
	def next_char(self) -> str:
		self.pos += 1
		self.column += 1
		return self.content[self.pos]

	def back(self) -> None:
		self.pos -= 1
		self.column -= 1

	def is_eof(self) -> bool:
		if self.pos >= len(self.content)-1:
			return True
		return False


def is_letter(char: str) -> bool:
	return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')

def is_digit(char: str) -> bool:
	return char >= '0' and char <= '9'

def is_inline_comment(char: str) -> bool:
	return char == '#'

def is_space(char: str) -> bool:
	return char in [' ', '\t', '\r']
	
def end_of_line(char: str) -> bool:
	return char == '\n'

def is_relational_operator(char: str) -> bool:
	return char in ['=', '>', '<', '!']

def is_arithmetic_operator(char: str) -> bool:
	return char in ['+', '-', '*', '/']

def is_assignment_operator(char: str) -> bool:
	return char == '='

def open_parenthesis(char: str) -> bool:
	return char == '('

def close_parenthesis(char: str) -> bool:
	return char == ')'


