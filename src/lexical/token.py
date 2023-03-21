from utils.token_type import TokenType


class Token:
    
	def __init__(self, type: TokenType, content: str):
		self.type = type
		self.content = content

	def __str__(self):
		return f"Token [type={self.type}, content={self.content}]"

	def __repr__(self):
		return self.__str__()
