from utils.scanner import Scanner
from utils.grammar import Grammar, Terminal
from utils.error import SyntaxError
from utils.token import Token

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.grammar = Grammar()
        self.reset()

    def reset(self):
        self.grammar.reset()
        self.has_reached_eof = False

    def _get_current_state(self):
        return self.grammar.get_current_state()

    def _get_next_token(self):
        token_type, token_str, is_eof = None, '', False
        while not is_eof and token_type not in Grammar.grammar_tokens:
            token_type, token_str, is_eof = self.scanner.get_next_token()
        return token_type, token_str, is_eof

    def _get_terminal_by_token(self, token_type, token_str):
        if token_type == Token.NUM:
            return Terminal.NUM
        elif token_type == Token.ID:
            return Terminal.ID
        elif token_type == Token.KEYWORD:
            for terminal in Grammar.keyword_terminals:
                if token_str == terminal.value:
                    return terminal
            else:
                return None
        elif token_type == Token.SYMBOL:
            for terminal in Grammar.symbol_terminals:
                if token_str == terminal.value:
                    return terminal
            else:
                return None
        elif token_type == Token.DOLLAR:
            return Terminal.DOLLAR
        else:
            return None

    def proceed(self):
        token_type, token_str, is_eof = self._get_next_token()
        if is_eof:
            self.has_reached_eof = True
            if not self.grammar.is_final():
                raise SyntaxError('Unexpected EOF')
            return False
        terminal = self._get_terminal_by_token(token_type, token_str)
        success = self.grammar.proceed(terminal)
        if not success:
            current_state = self.grammar.get_current_state()
            if self.grammar.is_terminal_state():
                raise SyntaxError(f'missing {terminal.value}')
            elif terminal in current_state.get_follow():
                raise SyntaxError(f'missing {current_state.name}')
            else:
                raise SyntaxError(f'illegal {terminal.value}')
        return True

    def eof_reached(self):
        return self.has_reached_eof