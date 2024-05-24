from utils.scanner import Scanner
from utils.grammar import Grammar, Terminal
from utils.error import UnexpectedEOFError, MissingSymbolError
from utils.token import Token

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.grammar = Grammar()
        self.reset()

    def reset(self):
        self.grammar.reset()
        self.has_reached_eof = False
        self.has_missing_symbol_error = False

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
        if not self.has_missing_symbol_error:
            self.token_type, self.token_str, self.is_eof = self._get_next_token()
        self.has_missing_symbol_error = False
        if self.grammar.eof_reached():
            self.has_reached_eof = True
            return
        terminal = self._get_terminal_by_token(self.token_type, self.token_str)
        if terminal:
            try:
                self.grammar.proceed(terminal, self.token_str)
            except MissingSymbolError as me:
                self.has_missing_symbol_error = True
                raise me
            except UnexpectedEOFError as ue:
                self.has_reached_eof = True
                raise ue

    def eof_reached(self):
        return self.has_reached_eof

    def get_root_node(self):
        return self.grammar.get_root_node()