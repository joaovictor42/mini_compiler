from enum import Enum

class CompileLexicalError(Exception):
	def __init__(self, type: str, line: int, column: int):
		self.message = f"{type}\nLine: {line} Column: {column}"

class LexicalError(Enum):
	RELATIONAL_OPERATOR_MALFORMED = 1
	NUMBER_MALFORMED = 2
	INVALID_CHARACTER = 3