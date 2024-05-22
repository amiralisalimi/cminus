class CompileError(Exception):
    msg = 'Compilation error'

    def __init__(self, text):
        super().__init__()
        self.text = text

class LexicalError(CompileError):
    msg = 'Lexical error'

    def __str__(self):
        return f'({self.text}, {self.msg})'

class InvalidInputError(LexicalError):
    msg = 'Invalid input'

class UnclosedCommentError(LexicalError):
    msg = 'Unclosed comment'

class UnmatchedCommentError(LexicalError):
    msg = 'Unmatched comment'

class InvalidNumberError(LexicalError):
    msg = 'Invalid number'


class SyntaxError(CompileError):
    msg = 'syntax error'

    def __str__(self):
        return f'{self.msg}, {self.text}'