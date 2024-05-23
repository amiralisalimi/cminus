"""
Amirali Salimi - 400109384
"""
from anytree import RenderTree
from utils.scanner import Scanner
from utils.token import Token
from utils.error import SyntaxError
from utils.parser import Parser

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

def write_syntax_error(fd_serr, syntax_error, lineno):
    fd_serr.write(f'#{lineno} : {syntax_error}\n')

def write_symbols(fd_sym, lexemes):
    if len(lexemes):
        lineno = 1
        for lexeme in lexemes:
            fd_sym.write(str(lineno) + '.\t' + lexeme + '\n')
            lineno += 1

def write_parse_tree(fd_ptree, root):
    for pre, fill, node in RenderTree(root):
        fd_ptree.write(f'{pre}{node.name}\n')

def run():
    with open('input.txt', 'r') as fd_in, \
        open('parse_tree.txt', 'w', encoding='utf-8') as fd_ptree, \
        open('syntax_errors.txt', 'w') as fd_serr:
        scanner = Scanner(fd_in)
        parser = Parser(scanner)
        error_found = False
        while not parser.eof_reached():
            try:
                parser.proceed()
            except SyntaxError as se:
                error_found = True
                write_syntax_error(fd_serr, se, scanner.get_lineno())
        if not error_found:
            fd_serr.write('There is no syntax error.')
        write_parse_tree(fd_ptree, parser.get_root_node())

if __name__ == '__main__':
    run()