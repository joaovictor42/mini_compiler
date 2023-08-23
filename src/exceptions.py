from enum import Enum

class LexicalError(Enum):
	RELATIONAL_OPERATOR_MALFORMED = 1
	NUMBER_MALFORMED = 2
	INVALID_CHARACTER = 3
	INDENTIFIER_MALFORMED = 4


class LexicalException(Exception):
	def __init__(self, message):
		self.message = message


class SyntaxException(Exception):
	def __init__(self, message):
		self.message = message