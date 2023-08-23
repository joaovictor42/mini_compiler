from enum import Enum

class TokenType(Enum):
    IDENTYFIER = 0
    NUMBER = 1
    ASSIGNMENT = 2
    RELATIONAL_OPERATOR = 3
    ARITHMETIC_OPERATOR = 4
    LEFT_PARENTHESIS = 5
    RIGHT_PARENTHESIS = 6
    RESERVED = 7