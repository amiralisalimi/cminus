from enum import Enum
from utils.token import Token, Character

class State:
    def __init__(self, is_lookahead, is_final, error = False, token_type = None):
        self.lookahead = is_lookahead
        self.final = is_final
        self.error = error
        self.token_type = token_type
    
    def is_lookahead(self):
        return self.lookahead

    def is_final(self):
        return self.final
    
    def has_error(self):
        return self.error
    
    def get_token_type(self):
        return self.token_type

class DFA:
    class States(Enum):
        INIT = State(False, False)
        TRASH = State(False, True, True)

        NUM = State(False, False)
        NUM_FINAL = State(True, True, False, Token.NUM)
        NUM_INVALID = State(False, True, True)

        SYM = State(False, True, False, Token.SYMBOL)
        ASSIGN = State(False, False)
        EQUAL = State(False, False, False, Token.SYMBOL)
        SYM_FINAL = State(True, True, False, Token.SYMBOL)

        KEY = State(False, False)
        KEY_FINAL = State(True, True, False, Token.KEYWORD)

        WHS = State(False, False)
        WHS_Final = State(True, True, False, Token.WHITESPACE)

        COM_SLASH = State(False, False)
        COM_STAR = State(False, False)
        COM_OPEN = State(False, False)
        COM_CLOSE = State(False, False)
        COM_FINAL = State(False, True, False, Token.COMMENT)
        COM_UNMATCHED = State(False, True, True, Token.COMMENT)

    transitions = [
        (States.INIT, '/', States.COM_SLASH),
        (States.COM_SLASH, '*', States.COM_OPEN),
        (States.COM_OPEN, '*', States.COM_CLOSE),
        (States.COM_OPEN, Character.all, States.COM_OPEN),
        (States.COM_CLOSE, '/', States.COM_FINAL),
        (States.COM_CLOSE, '*', States.COM_CLOSE),
        (States.COM_CLOSE, Character.all, States.COM_OPEN),
        (States.INIT, '*', States.COM_STAR),
        (States.COM_STAR, '/', States.COM_UNMATCHED),
        (States.COM_STAR, Character.digits + Character.nondigits + ';', States.SYM_FINAL),

        (States.INIT, Character.digits, States.NUM),
        (States.NUM, Character.digits, States.NUM),
        (States.NUM, Character.whitespace + Character.symbols, States.NUM_FINAL),
        (States.NUM, Character.letters, States.NUM_INVALID),

        (States.INIT, '=', States.ASSIGN),
        (States.INIT, Character.symbols, States.SYM),
        (States.ASSIGN, '=', States.EQUAL),
        (States.ASSIGN, Character.digits + Character.nondigits, States.SYM_FINAL),
        (States.EQUAL, Character.digits + Character.nondigits, States.SYM_FINAL),

        (States.INIT, Character.letters, States.KEY),
        (States.KEY, Character.alphanumeric, States.KEY),
        (States.KEY, Character.whitespace + Character.symbols, States.KEY_FINAL),

        (States.INIT, Character.whitespace, States.WHS),
        (States.WHS, Character.whitespace, States.WHS),
        (States.WHS, Character.all, States.WHS_Final)
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_state = self.States.INIT

    def proceed(self, next_char: str):
        for state, char_class, to_state in self.transitions:
            if state == self.current_state and next_char in char_class:
                self.current_state = to_state
                return True
        self.current_state = self.States.TRASH
        return False

    def has_error(self):
        return self.current_state.value.has_error()

    def is_acceptable(self):
        return not self.current_state.value.has_error() and \
                    self.current_state != self.States.COM_OPEN and \
                    self.current_state != self.States.COM_CLOSE

    def is_final(self):
        return self.current_state.value.is_final()

    def is_lookahead(self):
        return self.current_state.value.is_lookahead()

    def get_token_type(self):
        return self.current_state.value.get_token_type()

    def get_current_state(self):
        return self.current_state