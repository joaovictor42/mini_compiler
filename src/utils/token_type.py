from enum import Enum

class TokenType(Enum):
    VARIAVEL = 0
    INTEIRO = 1
    REAL = 2
    ASSIGNMENT = 3
    RELATIONAL_OPERATOR = 4
    ARITHMETIC_OPERATOR = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7
    SEMICOLON = 8
    COMMA = 9
    COLON = 10
    RESERVED = 11
    CADEIA = 12