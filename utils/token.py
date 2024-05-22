import string
from enum import Enum

class Token(Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6
    DOLLAR = 7

class Character:
    digits = '0123456789'
    whitespace = ' \t\n\r\v\f'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = lowercase + uppercase
    symbols = ';:,[]()\{\}+-*<=/'

    keywords =  ['if', 'else', 'void', 'int', 'for', 'break', 'return', 'endif']

    alphanumeric = letters + digits
    nondigits = whitespace + letters + symbols
    all = string.printable