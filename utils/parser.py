from utils.scanner import Scanner
from utils.grammar import Grammar

class Parser:
    def __init__(self, scanner: Scanner, grammar: Grammar):
        self.scanner = scanner
        self.grammar = grammar

    def _reset(self):
        self.grammar.reset()

    def _get_current_state(self):
        return self.grammar.get_current_state()

    def _get_next_token(self):
        token_type, token_str, is_eof = None, '', False
        while not is_eof and token_type not in Grammar.grammar_tokens:
            token_type, token_str, is_eof = self.scanner.get_next_token()
        return token_type, token_str, is_eof

    def proceed(self):
        token_type, token_str, is_eof = self._get_next_token()