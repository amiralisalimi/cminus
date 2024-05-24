from enum import Enum
from anytree import Node
from utils.token import Token
from utils.error import MissingSymbolError, IllegalTerminalError, UnexpectedEOFError

class Terminal(Enum):
    ID = 'ID'
    NUM = 'NUM'
    EPSILON = 'epsilon'

    IF = 'if'
    ELSE = 'else'
    VOID = 'void'
    INT = 'int'
    FOR = 'for'
    BREAK = 'break'
    RETURN = 'return'
    ENDIF = 'endif'

    COLON = ':'
    SEMICOLON = ';'
    OPEN_PARENTHESIS = '('
    CLOSE_PARENTHESIS = ')'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    OPEN_CURLY_BRACKET = '{'
    CLOSE_CURLY_BRACKET = '}'
    COMMA = ','
    EQUAL = '=='
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    LESS = '<'

    DOLLAR = '$'

    def get_name(self, lexeme=None):
        if self in Grammar.keyword_terminals:
            return f'(KEYWORD, {self.value})'
        elif self in Grammar.symbol_terminals:
            return f'(SYMBOL, {self.value})'
        elif self in [Terminal.ID, Terminal.NUM]:
            return f'({self.value}, {lexeme})'
        else:
            return self.value

class NonTerminal:
    def __init__(self, name, first, follow):
        self.name = name
        self.first = first
        self.follow = follow

    def get_name(self):
        return self.name

    def get_first(self):
        return self.first

    def get_follow(self):
        return self.follow

class Grammar:
    class States(Enum):
        Program = NonTerminal('Program', [Terminal.INT, Terminal.VOID, Terminal.EPSILON], [Terminal.DOLLAR])
        Declaration_list = NonTerminal('Declaration-list', [Terminal.INT, Terminal.VOID, Terminal.EPSILON], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Declaration = NonTerminal('Declaration', [Terminal.INT, Terminal.VOID], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.INT, Terminal.VOID, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Declaration_initial = NonTerminal('Declaration-initial', [Terminal.INT, Terminal.VOID], [Terminal.SEMICOLON, Terminal.OPEN_BRACKET, Terminal.OPEN_PARENTHESIS, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Declaration_prime = NonTerminal('Declaration-prime', [Terminal.SEMICOLON, Terminal.OPEN_BRACKET, Terminal.OPEN_PARENTHESIS], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.INT, Terminal.VOID, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Var_declaration_prime = NonTerminal('Var-declaration-prime', [Terminal.SEMICOLON, Terminal.OPEN_BRACKET], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.INT, Terminal.VOID, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Fun_declaration_prime = NonTerminal('Fun-declaration-prime', [Terminal.OPEN_PARENTHESIS], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.INT, Terminal.VOID, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Type_specifier = NonTerminal('Type-specifier', [Terminal.INT, Terminal.VOID], [Terminal.ID])
        Params = NonTerminal('Params', [Terminal.INT, Terminal.VOID], [Terminal.CLOSE_PARENTHESIS])
        Param_list = NonTerminal('Param-list', [Terminal.COMMA, Terminal.EPSILON], [Terminal.CLOSE_PARENTHESIS])
        Param = NonTerminal('Param', [Terminal.INT, Terminal.VOID], [Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Param_prime = NonTerminal('Param-prime', [Terminal.OPEN_BRACKET, Terminal.EPSILON], [Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Compound_stmt = NonTerminal('Compound-stmt', [Terminal.OPEN_CURLY_BRACKET], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.INT, Terminal.VOID, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.DOLLAR])
        Statement_list = NonTerminal('Statement-list', [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS, Terminal.EPSILON], [Terminal.CLOSE_CURLY_BRACKET])
        Statement = NonTerminal('Statement', [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Expression_stmt = NonTerminal('Expression-stmt', [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.BREAK, Terminal.PLUS, Terminal.MINUS], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Selection_stmt = NonTerminal('Selection-stmt', [Terminal.IF], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Else_stmt = NonTerminal('Else-stmt', [Terminal.ENDIF, Terminal.ELSE], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Iteration_stmt = NonTerminal('Iteration-stmt', [Terminal.FOR], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Return_stmt = NonTerminal('Return-stmt', [Terminal.RETURN], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Return_stmt_prime = NonTerminal('Return-stmt-prime', [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.PLUS, Terminal.MINUS])
        Expression = NonTerminal('Expression', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        B = NonTerminal('B', [Terminal.OPEN_BRACKET, Terminal.OPEN_PARENTHESIS, Terminal.ASSIGN, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        H = NonTerminal('H', [Terminal.ASSIGN, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Simple_expression_zegond = NonTerminal('Simple-expression-zegond', [Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Simple_expression_prime = NonTerminal('Simple-expression-prime', [Terminal.OPEN_PARENTHESIS, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        C = NonTerminal('C', [Terminal.LESS, Terminal.EQUAL, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Relop = NonTerminal('Relop', [Terminal.LESS, Terminal.EQUAL], [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS])
        Additive_expression = NonTerminal('Additive-expression', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA])
        Additive_expression_prime = NonTerminal('Additive-expression-prime', [Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL])
        Additive_expression_zegond = NonTerminal('Additive-expression-zegond', [Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL])
        D = NonTerminal('D', [Terminal.PLUS, Terminal.MINUS, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL])
        Addop = NonTerminal('Addop', [Terminal.PLUS, Terminal.MINUS], [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS])
        Term = NonTerminal('Term', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS])
        Term_prime = NonTerminal('Term-prime', [Terminal.OPEN_PARENTHESIS, Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS])
        Term_zegond = NonTerminal('Term-zegond', [Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS])
        G = NonTerminal('G', [Terminal.MULTIPLY, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS])
        Signed_factor = NonTerminal('Signed-factor', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Signed_factor_prime = NonTerminal('Signed-factor-prime', [Terminal.OPEN_PARENTHESIS, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Signed_factor_zegond = NonTerminal('Signed-factor-zegond', [Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Factor = NonTerminal('Factor', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Var_call_prime = NonTerminal('Var-call-prime', [Terminal.OPEN_BRACKET, Terminal.OPEN_PARENTHESIS, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Var_prime = NonTerminal('Var-prime', [Terminal.OPEN_BRACKET, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Factor_prime = NonTerminal('Factor-prime', [Terminal.OPEN_PARENTHESIS, Terminal.EPSILON], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Factor_zegond = NonTerminal('Factor-zegond', [Terminal.NUM, Terminal.OPEN_PARENTHESIS], [Terminal.SEMICOLON, Terminal.CLOSE_BRACKET, Terminal.CLOSE_PARENTHESIS, Terminal.COMMA, Terminal.LESS, Terminal.EQUAL, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY])
        Args = NonTerminal('Args', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS, Terminal.EPSILON], [Terminal.CLOSE_PARENTHESIS])
        Arg_list = NonTerminal('Arg-list', [Terminal.ID, Terminal.NUM, Terminal.OPEN_PARENTHESIS, Terminal.PLUS, Terminal.MINUS], [Terminal.CLOSE_PARENTHESIS])
        Arg_list_prime = NonTerminal('Arg-list-prime', [Terminal.COMMA, Terminal.EPSILON], [Terminal.CLOSE_PARENTHESIS])

        def get_name(self):
            return self.value.get_name()

        def get_first(self):
            return tuple(self.value.get_first())

        def get_follow(self):
            return tuple(self.value.get_follow())

    grammar_tokens = [Token.NUM, Token.ID, Token.KEYWORD, Token.SYMBOL, Token.DOLLAR]
    keyword_terminals = [Terminal.IF, Terminal.ELSE, Terminal.VOID, Terminal.INT, Terminal.FOR, Terminal.BREAK, Terminal.RETURN, Terminal.ENDIF]
    symbol_terminals = [Terminal.COLON, Terminal.SEMICOLON, Terminal.OPEN_PARENTHESIS, Terminal.CLOSE_PARENTHESIS, Terminal.OPEN_BRACKET, Terminal.CLOSE_BRACKET, Terminal.OPEN_CURLY_BRACKET, Terminal.CLOSE_CURLY_BRACKET, Terminal.COMMA, Terminal.EQUAL, Terminal.ASSIGN, Terminal.PLUS, Terminal.MINUS, Terminal.MULTIPLY, Terminal.LESS]

    rules = {
        States.Program: {
            States.Declaration_list.get_first() + States.Program.get_follow(): [States.Declaration_list]
        },
        States.Declaration_list: {
            States.Declaration.get_first(): [States.Declaration, States.Declaration_list]
        },
        States.Declaration: {
            States.Declaration_initial.get_first(): [States.Declaration_initial, States.Declaration_prime]
        },
        States.Declaration_initial: {
            States.Type_specifier.get_first(): [States.Type_specifier, Terminal.ID]
        },
        States.Declaration_prime: {
            States.Fun_declaration_prime.get_first(): [States.Fun_declaration_prime],
            States.Var_declaration_prime.get_first(): [States.Var_declaration_prime]
        },
        States.Var_declaration_prime: {
            (Terminal.SEMICOLON,): [Terminal.SEMICOLON],
            (Terminal.OPEN_BRACKET,): [Terminal.OPEN_BRACKET, Terminal.NUM, Terminal.CLOSE_BRACKET, Terminal.SEMICOLON]
        },
        States.Fun_declaration_prime: {
            (Terminal.OPEN_PARENTHESIS,): [Terminal.OPEN_PARENTHESIS, States.Params, Terminal.CLOSE_PARENTHESIS, States.Compound_stmt]
        },
        States.Type_specifier: {
            (Terminal.INT,): [Terminal.INT],
            (Terminal.VOID,): [Terminal.VOID]
        },
        States.Params: {
            (Terminal.INT,): [Terminal.INT, Terminal.ID, States.Param_prime, States.Param_list],
            (Terminal.VOID,): [Terminal.VOID]
        },
        States.Param_list: {
            (Terminal.COMMA,): [Terminal.COMMA, States.Param, States.Param_list]
        },
        States.Param: {
            States.Declaration_initial.get_first(): [States.Declaration_initial, States.Param_prime]
        },
        States.Param_prime: {
            (Terminal.OPEN_BRACKET,): [Terminal.OPEN_BRACKET, Terminal.CLOSE_BRACKET]
        },
        States.Compound_stmt: {
            (Terminal.OPEN_CURLY_BRACKET,): [Terminal.OPEN_CURLY_BRACKET, States.Declaration_list, States.Statement_list,
                                    Terminal.CLOSE_CURLY_BRACKET]
        },
        States.Statement_list: {
            States.Statement.get_first(): [States.Statement, States.Statement_list]
        },
        States.Statement: {
            States.Return_stmt.get_first(): [States.Return_stmt],
            States.Expression_stmt.get_first(): [States.Expression_stmt],
            States.Compound_stmt.get_first(): [States.Compound_stmt],
            States.Selection_stmt.get_first(): [States.Selection_stmt],
            States.Iteration_stmt.get_first(): [States.Iteration_stmt]
        },
        States.Expression_stmt: {
            States.Expression.get_first(): [States.Expression, Terminal.SEMICOLON],
            (Terminal.BREAK,): [Terminal.BREAK, Terminal.SEMICOLON],
            (Terminal.SEMICOLON,): [Terminal.SEMICOLON]
        },
        States.Selection_stmt: {
            (Terminal.IF,): [Terminal.IF, Terminal.OPEN_PARENTHESIS, States.Expression, Terminal.CLOSE_PARENTHESIS,
                                States.Statement, States.Else_stmt]
        },
        States.Else_stmt: {
            (Terminal.ENDIF,): [Terminal.ENDIF],
            (Terminal.ELSE,): [Terminal.ELSE, States.Statement, Terminal.ENDIF]
        },
        States.Iteration_stmt: {
            (Terminal.FOR,): [Terminal.FOR, Terminal.OPEN_PARENTHESIS, States.Expression, Terminal.SEMICOLON,
                                    States.Expression, Terminal.SEMICOLON, States.Expression, Terminal.CLOSE_PARENTHESIS,
                                    States.Statement]
        },
        States.Return_stmt: {
            (Terminal.RETURN,): [Terminal.RETURN, States.Return_stmt_prime]
        },
        States.Return_stmt_prime: {
            States.Expression.get_first(): [States.Expression, Terminal.SEMICOLON],
            (Terminal.SEMICOLON,): [Terminal.SEMICOLON]
        },
        States.Expression: {
            States.Simple_expression_zegond.get_first(): [States.Simple_expression_zegond],
            (Terminal.ID,): [Terminal.ID, States.B]
        },
        States.B: {
            (Terminal.ASSIGN,): [Terminal.ASSIGN, States.Expression],
            (Terminal.OPEN_BRACKET,): [Terminal.OPEN_BRACKET, States.Expression, Terminal.CLOSE_BRACKET, States.H],
            (States.Simple_expression_prime.get_first() + States.B.get_follow()): [
                States.Simple_expression_prime]
        },
        States.H: {
            (Terminal.ASSIGN,): [Terminal.ASSIGN, States.Expression],
            (States.G.get_first() + States.D.get_first() + States.C.get_first() + States.H.get_follow()): [
                States.G, States.D, States.C]
        },
        States.Simple_expression_zegond: {
            States.Additive_expression_zegond.get_first(): [States.Additive_expression_zegond, States.C]
        },
        States.Simple_expression_prime: {
            (States.Additive_expression_prime.get_first() + States.C.get_first() 
             + States.Simple_expression_prime.get_follow()): [
                States.Additive_expression_prime, States.C]
        },
        States.C: {
            States.Relop.get_first(): [States.Relop, States.Additive_expression]
        },
        States.Relop: {
            (Terminal.LESS,): [Terminal.LESS],
            (Terminal.EQUAL,): [Terminal.EQUAL, ]
        },
        States.Additive_expression: {
            States.Term.get_first(): [States.Term, States.D]
        },
        States.Additive_expression_prime: {
            (
                States.Term_prime.get_first() + States.D.get_first() + States.Additive_expression_prime.get_follow()): [
                States.Term_prime, States.D]
        },
        States.Additive_expression_zegond: {
            States.Term_zegond.get_first(): [States.Term_zegond, States.D]
        },
        States.D: {
            States.Addop.get_first(): [States.Addop, States.Term, States.D]
        },
        States.Addop: {
            (Terminal.PLUS,): [Terminal.PLUS],
            (Terminal.MINUS,): [Terminal.MINUS]
        },
        States.Term: {
            States.Signed_factor.get_first(): [States.Signed_factor, States.G]
        },
        States.Term_prime: {
            (States.Signed_factor_prime.get_first() + States.G.get_first() + States.Term_prime.get_follow()): [
                States.Signed_factor_prime, States.G]
        },
        States.Term_zegond: {
            States.Signed_factor_zegond.get_first(): [States.Signed_factor_zegond, States.G]
        },
        States.G: {
            (Terminal.MULTIPLY,): [Terminal.MULTIPLY, States.Signed_factor, States.G]
        },
        States.Signed_factor: {
            (Terminal.PLUS,): [Terminal.PLUS, States.Factor],
            (Terminal.MINUS,): [Terminal.MINUS, States.Factor],
            States.Factor.get_first(): [States.Factor]
        },
        States.Signed_factor_prime: {
            (States.Factor_prime.get_first() + States.Signed_factor_prime.get_follow()): [
                States.Factor_prime]
        },
        States.Signed_factor_zegond: {
            (Terminal.PLUS,): [Terminal.PLUS, States.Factor],
            (Terminal.MINUS,): [Terminal.MINUS, States.Factor],
            States.Factor_zegond.get_first(): [States.Factor_zegond]
        },
        States.Factor: {
            (Terminal.OPEN_PARENTHESIS,): [Terminal.OPEN_PARENTHESIS, States.Expression, Terminal.CLOSE_PARENTHESIS],
            (Terminal.ID,): [Terminal.ID, States.Var_call_prime],
            (Terminal.NUM,): [Terminal.NUM]
        },
        States.Var_call_prime: {
            (Terminal.OPEN_PARENTHESIS,): [Terminal.OPEN_PARENTHESIS, States.Args, Terminal.CLOSE_PARENTHESIS],
            (States.Var_prime.get_first() + States.Var_call_prime.get_follow()): [States.Var_prime]
        },
        States.Var_prime: {
            (Terminal.OPEN_BRACKET,): [Terminal.OPEN_BRACKET, States.Expression, Terminal.CLOSE_BRACKET]
        },
        States.Factor_prime: {
            (Terminal.OPEN_PARENTHESIS,): [Terminal.OPEN_PARENTHESIS, States.Args, Terminal.CLOSE_PARENTHESIS]
        },
        States.Factor_zegond: {
            (Terminal.OPEN_PARENTHESIS,): [Terminal.OPEN_PARENTHESIS, States.Expression, Terminal.CLOSE_PARENTHESIS],
            (Terminal.NUM,): [Terminal.NUM]
        },
        States.Args: {
            States.Arg_list.get_first(): [States.Arg_list]
        },
        States.Arg_list: {
            States.Expression.get_first(): [States.Expression, States.Arg_list_prime]
        },
        States.Arg_list_prime: {
            (Terminal.COMMA,): [Terminal.COMMA, States.Expression, States.Arg_list_prime]
        }
    }

    def __init__(self):
        self.reset()

    def reset(self):
        self.state_stack = [self.States.Program]
        self.root_node = Node(self.get_current_state().get_name())
        self.node_stack = [self.root_node]
        self.has_reached_eof = False

    def is_terminal_state(self, state=None):
        return isinstance(state if state else self.get_current_state(), Terminal)

    def _clear_unused_nodes(self, current_node=None):
        if not current_node:
            for node in self.node_stack:
                node.parent = None
            return
        while current_node:
            parent_node = current_node.parent
            current_node.parent = None
            if not parent_node.children:
                current_node = parent_node
            else:
                current_node = None
        return

    def _apply(self, rule=None):
        self.state_stack.pop()
        parent_node = self.node_stack.pop()
        if rule:
            current_node_list = [Node(var.get_name(), parent_node) for var in rule]
            for var in reversed(rule):
                self.state_stack.append(var)
            self.node_stack.extend(reversed(current_node_list))

    def _match(self, terminal):
        current_state = self.get_current_state()
        self._apply()
        if terminal == current_state:
            return True
        raise MissingSymbolError(current_state.value)

    def proceed(self, terminal: Terminal, lexeme=None):
        if self.is_final():
            self.has_reached_eof = True
            Node(Terminal.DOLLAR.get_name(), self.get_root_node())
            self._clear_unused_nodes()
            return True
        current_state = self.get_current_state()
        current_node = self.get_current_node()
        if self.is_terminal_state():
            try:
                ret_value = self._match(terminal)
                current_node.name = terminal.get_name(lexeme)
                return ret_value
            except MissingSymbolError as me:
                self._clear_unused_nodes(current_node)
                raise me
        for possible_terminals, rule in self.rules[current_state].items():
            if terminal in possible_terminals:
                self._apply(rule)
                return self.proceed(terminal, lexeme)
        else:
            if Terminal.EPSILON in current_state.get_first() \
                and terminal in current_state.get_follow():
                self._apply()
                Node(Terminal.EPSILON.get_name(), current_node)
                return self.proceed(terminal, lexeme)
            elif terminal in current_state.get_follow():
                self._clear_unused_nodes(current_node)
                self._apply()
                raise MissingSymbolError(current_state.get_name())
            elif terminal == Terminal.DOLLAR:
                self.has_reached_eof = True
                self._clear_unused_nodes()
                raise UnexpectedEOFError()
            else:
                raise IllegalTerminalError(terminal.value)

    def get_current_state(self):
        if self.state_stack:
            return self.state_stack[-1]
        return None

    def get_current_node(self):
        if self.node_stack:
            return self.node_stack[-1]
        return None

    def is_final(self):
        return not self.state_stack

    def eof_reached(self):
        return self.has_reached_eof

    def get_root_node(self):
        return self.root_node