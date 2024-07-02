from enum import Enum
from utils.symbol_table import SymbolTable

class ActionSymbol(Enum):
    PUSH_ID = '_push_id'
    BEGIN_FUNC = '_begin_func'
    END_FUNC = '_end_func'
    BEGIN_BLOCK = '_begin_block'
    END_BLOCK = '_end_block'
    DEFINE_INT = '_define_int'
    DEFINE_ARR = '_define_arr'
    PUSH_STACK = '_push_stack'
    POP_STACK = '_pop_stack'
    ASSIGN = '_assign'
    OPERATION = '_operation'
    NEGATE = '_negate'
    PUSH_LINENO = '_push_lineno'
    SKIP_PB = '_skip_pb'
    JPF_FROM_SKIPPED1 = '_jpf_from_skipped1'
    JPF_FROM_SKIPPED2 = '_jpf_from_skipped2'
    JP_FROM_SKIPPED1 = '_jp_from_skipped1'
    JP_FROM_SKIPPED2 = '_jp_from_skipped2'
    JP_TO_SKIPPED1 = '_jp_to_skipped1'
    JP_TO_SKIPPED4 = '_jp_to_skipped4'
    REGISTER_FUNC = '_register_func'
    ADD_FUNC_PARAM = '_add_func_param'
    PARAM_TYPE_TO_ARR = '_param_type_to_arr'
    CALL_FUNC = '_call_func'
    CALL_MAIN = '_call_main'
    PUSH_FP_VALUE = '_push_fp_value'
    RETURN_CODE_BLOCK = '_return_code_block'
    FUNC_RETURN = '_func_return'
    SET_FUNC_RETURN_VALUE = '_set_func_return_value'
    PUSH_ARR_INDEX_ADDR = '_push_arr_index_addr'
    PUSH_ADDR_VALUE = '_push_addr_value'
    ARR_ASSIGN = '_arr_assign'
    BEGIN_LOOP = '_begin_loop'
    END_LOOP = '_end_loop'
    BREAK_STATEMENT = '_break_statement'
    BEGIN_ARGS = '_begin_args'
    POP_SS = '_pop_ss'

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

class CodeGenerator:

    SP = 500
    FP = SP + 4
    TEMP = FP + 4
    STACK = TEMP + 4

    def __init__(self):
        self.reset()

    def reset(self):
        self.SS = []
        self.PB = []
        self.global_table = SymbolTable()
        self.func_table = SymbolTable()
        self.funcs = {
            'output': ('void', None, [('input', 'int')])
        }
        self.curr_func = None
        self.return_block_lineno = None
        self.loop_blocks = []

        self.emit(f'ASSIGN, #{self.STACK}, {self.SP}, ')
        self.emit(f'ASSIGN, #{self.STACK}, {self.FP}, ')

        self.semantic_errors = []
    
    def emit(self, code=''):
        self.PB.append(code)

    def add_semantic_error(self, error, lineno):
        self.semantic_errors.append((error, lineno))

    def get_semantic_errors(self):
        return self.semantic_errors

    def get_pb(self):
        return self.PB

    def set_push_code(self, lineno, value):
        if value is not None:
            self.PB[lineno] = (f'ASSIGN, {value}, @{self.SP}, ')
            lineno += 1
        self.PB[lineno] = (f'ADD, {self.SP}, #4, {self.SP}')

    def pop_code(self):
        self.emit(f'SUB, {self.SP}, #4, {self.SP}')

    def push_code(self, value):
        lineno = len(self.PB)
        if value is not None: self.emit()
        self.emit(())
        self.set_push_code(lineno, value)

    def code_gen(self, name, lookahead, input_lineno):
        return self.__getattribute__(name)(lookahead, input_lineno)

    def _push_id(self, lookahead, input_lineno):
        self.SS.append(lookahead)

    def _begin_func(self, lookahead, input_lineno):
        self.func_table = SymbolTable(0)
        for param_name, param_type in self.funcs[self.curr_func][2]:
            self.func_table.add_symbol(param_name, 1 if param_type == 'array' else None, True)

    def _end_func(self, lookahead, input_lineno):
        self.func_table = None

    def _begin_block(self, lookahead, input_lineno):
        self.func_table.push_empty_stack()

    def _end_block(self, lookahead, input_lineno):
        self.func_table.pop_stack()

    def _define_int(self, lookahead, input_lineno):
        name = self.SS.pop()
        type = self.SS.pop()
        if type != 'int':
            self.add_semantic_error(f'Illegal type of void for \'{name}\'.', input_lineno)
        if self.func_table is None:
            self.global_table.add_symbol(name)
        else:
            self.func_table.add_symbol(name)
            self.push_code(None)

    def _define_arr(self, lookahead, input_lineno):
        size = int(self.SS.pop())
        name = self.SS.pop()
        type = self.SS.pop()
        if self.func_table is None:
            self.global_table.add_symbol(name, size)
        else:
            self.func_table.add_symbol(name, size)
        self.emit(f'ADD, {self.SP}, #{4 * size}, {self.SP}')

    def _push_stack(self, lookahead, input_lineno):
        token = self.SS.pop()
        if token.isdigit():
            self.push_code(f'#{token}')
            self.SS.append('int')
        else:
            symbol = self.func_table.get_symbol(token)
            if symbol is None:
                symbol = self.global_table.get_symbol(token)
                if symbol is None:
                    self.add_semantic_error(f'\'{token}\' is not defined.', input_lineno)
                    self.SS.append('int')
                    return
                else:
                    self.push_code(f'{symbol[0]}' if symbol[1] is None else f'#{symbol[0]}')
            else:
                self.emit(f'ADD, {self.FP}, #{symbol[0]}, {self.TEMP}')
                self.push_code(f'@{self.TEMP}' if symbol[1] is None or symbol[2] else f'{self.TEMP}')
            self.SS.append('int' if symbol[1] is None else 'array')

    def _pop_stack(self, lookahead, input_lineno):
        self.pop_code()
        self.SS.pop()

    def _assign(self, lookahead, input_lineno):
        rhs_type = self.SS.pop()
        name = self.SS.pop()
        symbol = self.func_table.get_symbol(name)
        self.pop_code()
        if symbol is None:
            symbol = self.global_table.get_symbol(name)
            if symbol is None:
                self.add_semantic_error(f'\'{name}\' is not defined.', input_lineno)
                self.SS.append('int')
                return
            else:
                self.emit(f'ASSIGN, @{self.SP}, {symbol[0]}, ')
        else:
            self.emit(f'ADD, {self.FP}, #{symbol[0]}, {self.TEMP}')
            self.emit(f'ASSIGN, @{self.SP}, @{self.TEMP}, ')
        lhs_type = 'int' if symbol[1] is None else 'array'
        if rhs_type != lhs_type:
            self.add_semantic_error(f'Type mismatch in operands, Got {lhs_type} instead of {rhs_type}.', input_lineno)
        self.push_code(None)
        self.SS.append(rhs_type)

    def _operation(self, lookahead, input_lineno):
        opr_type1 = self.SS.pop()
        opr = self.SS.pop()
        opr_type2 = self.SS.pop()
        if opr_type1 != opr_type2:
            self.add_semantic_error(f'Type mismatch in operands, Got array instead of int.', input_lineno)
        self.pop_code()
        self.emit(f'SUB, {self.SP}, #4, {self.TEMP}')
        opr_code = ('ADD' if opr == '+' else \
                    'SUB' if opr == '-' else \
                    'MULT' if opr == '*' else \
                    'LT' if opr == '<' else 'EQ')
        self.emit(f'{opr_code}, @{self.TEMP}, @{self.SP}, @{self.TEMP}')
        self.SS.append('int')

    def _negate(self, lookahead, input_lineno):
        type = self.SS.pop()
        if type != 'int':
            self.add_semantic_error(f'Type mismatch in operands, Got array instead of int.', input_lineno)
        self.pop_code()
        self.emit(f'SUB, #0, @{self.SP}, @{self.SP}')
        self.push_code(None)
        self.SS.append('int')

    def _push_lineno(self, lookahead, input_lineno):
        lineno = len(self.PB)
        self.SS.append(lineno)

    def _skip_pb(self, lookahead, input_lineno):
        self.emit()

    def _jpf_from_skipped1(self, lookahead, input_lineno):
        pb_lineno = self.SS.pop()
        lineno = len(self.PB)
        self.PB[pb_lineno] = f'JPF, @{self.SP}, {lineno}, '

    def _jpf_from_skipped2(self, lookahead, input_lineno):
        pb_lineno = self.SS.pop(-2)
        lineno = len(self.PB)
        self.PB[pb_lineno] = f'JPF, @{self.SP}, {lineno}, '

    def _jp_from_skipped1(self, lookahead, input_lineno):
        pb_lineno = self.SS.pop()
        lineno = len(self.PB)
        self.PB[pb_lineno] = f'JP, {lineno}, , '

    def _jp_from_skipped2(self, lookahead, input_lineno):
        pb_lineno = self.SS.pop(-2)
        lineno = len(self.PB)
        self.PB[pb_lineno] = f'JP, {lineno}, , '

    def _jp_to_skipped1(self, lookahead, input_lineno):
        label = self.SS.pop()
        self.emit(f'JP, {label}, , ')

    def _jp_to_skipped4(self, lookahead, input_lineno):
        label = self.SS.pop(-4)
        self.emit(f'JP, {label}, , ')

    def _register_func(self, lookahead, input_lineno):
        func_name = self.SS.pop()
        return_type = self.SS.pop()
        self.curr_func = func_name
        lineno = len(self.PB)
        self.funcs[func_name] = (return_type, lineno, [])

    def _add_func_param(self, lookahead, input_lineno):
        param_name = self.SS.pop()
        param_type = self.SS.pop()
        self.funcs[self.curr_func][2].append((param_name, param_type))

    def _param_type_to_arr(self, lookahead, input_lineno):
        self.return_block_lineno = len(self.PB)
        self.emit(f'SUB, {self.FP}, #4, {self.SP}')
        self.emit(f'ASSIGN, @{self.SP}, {self.FP}, ')
        self.pop_code()
        self.emit(f'ASSIGN, @{self.SP}, {self.TEMP}, ')
        self.emit(f'JP, @{self.TEMP}, , ')

    def _call_func(self, lookahead, input_lineno):
        args = []
        while self.SS[-1] != 'begin-args':
            args.append(self.SS.pop())
        args.reverse()
        self.SS.pop()
        pb_lineno = self.SS.pop()
        func_name = self.SS.pop()
        func = self.funcs[func_name]
        if len(args) != len(func[2]):
            self.add_semantic_error(f'Mismatch in numbers of arguments of \'{func_name}\'.', input_lineno)
        func_param_types = [param[1] for param in func[2]]
        for i in range(len(args)):
            arg = args[i]
            expected = func_param_types[i]
            if arg != expected:
                self.add_semantic_error(f'Mismatch in type of argument {i+1} of \'{func_name}\'. Expected \'{expected}\' but got \'{arg}\' instead.', input_lineno)
        if func_name == 'output':
            self._output(pb_lineno)
            return
        self.set_push_code(pb_lineno, None)
        self.emit(f'SUB, {self.SP}, #{4 * len(func[2])}, {self.FP}')
        self.emit(f'JP, {func[1]}, , ')
        lineno = len(self.PB)
        self.set_push_code(pb_lineno+1, f'#{lineno}')
        if func[0] == 'void':
            self.pop_code()
        self.SS.append('int')

    def _call_main(self, lookahead, input_lineno):
        pb_lineno = self.SS.pop()
        lineno = len(self.PB)
        self.set_push_code(pb_lineno, f'#{lineno}')
        self.PB[pb_lineno + 4] = f'ASSIGN, {self.SP}, {self.FP}, '
        self.PB[pb_lineno + 5] = f'JP, {self.funcs["main"][1]}, , '

    def _push_fp_value(self, lookahead, input_lineno):
        self.push_code(f'{self.FP}')

    def _return_code_block(self, lookahead, input_lineno):
        self.return_block_lineno = len(self.PB)
        self.emit(f'SUB, {self.FP}, #4, {self.SP}')
        self.emit(f'ASSIGN, @{self.SP}, {self.FP}, ')
        self.pop_code()
        self.emit(f'ASSIGN, @{self.SP}, {self.TEMP}, ')
        self.emit(f'JP, @{self.TEMP}, , ')

    def _func_return(self, lookahead, input_lineno):
        self.emit(f'JP, {self.return_block_lineno}, , ')

    def _set_func_return_value(self, lookahead, input_lineno):
        self.pop_code()
        self.SS.pop()
        self.emit(f'SUB, {self.FP}, #12, {self.TEMP}')
        self.emit(f'ASSIGN, @{self.SP}, @{self.TEMP}, ')

    def _push_arr_index_addr(self, lookahead, input_lineno):
        type = self.SS.pop()
        if type != 'int':
            self.add_semantic_error(f'Type mismatch in operands, Got array instead of int.', input_lineno)
        token = self.SS.pop()
        symbol = self.func_table.get_symbol(token)
        self.pop_code()
        self.emit(f'MULT, @{self.SP}, #4, @{self.SP}')
        if symbol is None:
            symbol = self.global_table.get_symbol(token)
            self.emit(f'ADD, #{symbol[0]}, @{self.SP}, {self.TEMP}')
            self.push_code(f'{self.TEMP}')
        else:
            self.emit(f'ADD, {self.FP}, #{symbol[0]}, {self.TEMP}')
            if symbol[2]:
                self.emit(f'ADD, @{self.TEMP}, @{self.SP}, {self.TEMP}')
            else:
                self.emit(f'ADD, {self.TEMP}, @{self.SP}, {self.TEMP}')
            self.push_code(f'{self.TEMP}')
        self.SS.append('int')

    def _push_addr_value(self, lookahead, input_lineno):
        self.pop_code()
        self.emit(f'ASSIGN, @{self.SP}, {self.TEMP}, ')
        self.push_code(f'@{self.TEMP}')

    def _arr_assign(self, lookahead, input_lineno):
        rhs_type = self.SS.pop()
        self.SS.pop()
        if rhs_type != 'int':
            self.add_semantic_error(f'Type mismatch in operands, Got array instead of int.', input_lineno)
        self.pop_code()
        self.pop_code()
        self.emit(f'ASSIGN, @{self.SP}, {self.TEMP}, ')
        self.push_code(None)
        self.emit(f'ASSIGN, @{self.SP}, @{self.TEMP}, ')
        self.emit(f'ASSIGN, @{self.SP}, {self.TEMP}, ')
        self.pop_code()
        self.push_code(f'{self.TEMP}')
        self.SS.append('int')

    def _begin_loop(self, lookahead, input_lineno):
        self.loop_blocks.append([])

    def _end_loop(self, lookahead, input_lineno):
        lineno = len(self.PB)
        for break_stmt_line in self.loop_blocks[-1]:
            self.PB[break_stmt_line] = f'JP, {lineno}, , '
        self.loop_blocks.pop()

    def _break_statement(self, lookahead, input_lineno):
        if not self.loop_blocks:
            self.add_semantic_error('No \'for\' found for \'break\'.', input_lineno)
            return
        lineno = len(self.PB)
        self.loop_blocks[-1].append(lineno)
        self.emit()

    def _begin_args(self, lookahead, input_lineno):
        self.SS.append('begin-args')

    def _pop_ss(self, lookahead, input_lineno):
        self.SS.pop()

    def _output(self, pb_lineno):
        self.PB[pb_lineno] = f'ASSIGN, 0, 0, '
        self.PB[pb_lineno+1] = f'ASSIGN 0, 0, '
        self.PB[pb_lineno+2] = f'ASSING, 0, 0, '
        self.pop_code()
        self.emit(f'PRINT, @{self.SP}, , ')
        self.pop_code()
        self.SS.append('int')