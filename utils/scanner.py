from utils.dfa import DFA
from utils.token import Token, Character
from utils.error import (
    InvalidInputError, UnclosedCommentError, UnmatchedCommentError, InvalidNumberError
)

class Scanner:
    def __init__(self, file):
        self.file = file
        self.lineno = 1
        self.dfa = DFA()
        self.buffer = ''
        self.last_char = None
        self.is_lookahead = False
        self.lexemes = set(Character.keywords)

    def _next_char(self):
        if not self.is_lookahead:
            return self.file.read(1)
        self.is_lookahead = False
        return self.last_char

    def _reset(self):
        self.dfa.reset()
        self.buffer = ''
    
    def _raise_error(self, text):
        current_state = self.dfa.get_current_state()
        if current_state == self.dfa.States.TRASH:
            raise InvalidInputError(text)
        elif current_state == self.dfa.States.COM_OPEN or \
            current_state == self.dfa.States.COM_CLOSE:
            raise UnclosedCommentError(text[:7] + '...')
        elif current_state == self.dfa.States.COM_UNMATCHED:
            raise UnmatchedCommentError(text)
        elif current_state == self.dfa.States.NUM_INVALID:
            raise InvalidNumberError(text)

    def _proceed(self, char):
        self.dfa.proceed(char)
        self.last_char = char
        self.is_lookahead = self.dfa.is_lookahead()
        if not self.is_lookahead:
            self.lineno += (self.last_char == '\n')
            self.buffer += self.last_char
        return self.last_char

    def get_lineno(self):
        return self.lineno
    
    def get_lexemes(self):
        return self.lexemes

    def get_token_type(self):
        token_type = self.dfa.get_token_type()
        if token_type == Token.KEYWORD and self.buffer in Character.keywords:
            return Token.KEYWORD
        elif token_type != Token.KEYWORD:
            return token_type
        else:
            return Token.ID

    def get_next_token(self):
        self._reset()
        while not self.dfa.has_error() and not self.dfa.is_final():
            char = self._next_char()
            if not char:
                if self.dfa.is_acceptable():
                    return (None, None, True)
                self._raise_error(self.buffer)
            self._proceed(char)
        if self.dfa.has_error():
            self._raise_error(self.buffer)
        token_type = self.get_token_type()
        if token_type == Token.KEYWORD or token_type == Token.ID:
            self.lexemes.add(self.buffer)
        return (token_type, self.buffer, False)