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

def write_semantic_error(fd_smerr, semantic_error, lineno):
    fd_smerr.write(f'#{lineno} : Semantic Error! {semantic_error}\n')

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
        open('syntax_errors.txt', 'w') as fd_serr, \
        open('output.txt', 'w') as fd_out, \
        open('semantic_errors.txt', 'w') as fd_smerr:
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

        inter_code = parser.get_pb()
        counter = 0
        for three_addr_code in inter_code:
            fd_out.write(f'{counter}\t({three_addr_code})\n')
            counter += 1

        semantic_errors = parser.get_semantic_errors()
        if semantic_errors:
            for smerr, lineno in semantic_errors:
                write_semantic_error(fd_smerr, smerr, lineno)
        else:
            fd_smerr.write('The input program is semantically correct.')
if __name__ == '__main__':
    run()