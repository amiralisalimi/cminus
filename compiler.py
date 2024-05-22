"""
Amirali Salimi - 400109384
Mohammad Ali Mirzaei - 400109481
"""
from utils.scanner import Scanner
from utils.token import Token
from utils.error import LexicalError

def write_token(fd_tok, token_type, token_str, lineno, newline=False):
    if token_type == Token.WHITESPACE:
        if '\n' in token_str and not newline:
            fd_tok.write('\n')
            return True
    elif token_type != Token.COMMENT:
        if newline:
            fd_tok.write(str(lineno) + '.\t')
        fd_tok.write('(' + token_type.name + ', ' + token_str + ') ')
        return False
    return newline

def write_lexical_error(fd_err, lexical_error, lineno, last_err_line):
    if lineno != last_err_line:
        if last_err_line != 0:
            fd_err.write('\n')
        fd_err.write(str(lineno) + '.\t')
    fd_err.write(str(lexical_error) + ' ')

def write_symbols(fd_sym, lexemes):
    if len(lexemes):
        lineno = 1
        for lexeme in lexemes:
            fd_sym.write(str(lineno) + '.\t' + lexeme + '\n')
            lineno += 1

def run():
    with open('input.txt', 'r') as fd_in, \
        open('tokens.txt', 'w') as fd_tok, \
        open('lexical_errors.txt', 'w') as fd_err, \
        open('symbol_table.txt', 'w') as fd_sym:
        scanner = Scanner(fd_in)
        newline = True
        last_err_line = 0
        error_found = False
        while True:
            try:
                token_type, token_str, eof = scanner.get_next_token()
                if eof:
                    break
                if token_type and token_str:
                    newline = write_token(fd_tok, token_type, token_str, scanner.get_lineno(), newline)
            except LexicalError as le:
                error_found = True
                write_lexical_error(fd_err, le, scanner.get_lineno(), last_err_line)
                last_err_line = scanner.get_lineno()
        write_symbols(fd_sym, scanner.get_lexemes())
        if not error_found:
            fd_err.write('There is no lexical error.')

if __name__ == '__main__':
    run()