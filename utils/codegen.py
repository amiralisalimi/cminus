from enum import Enum

class ActionSymbol(Enum):
    GET_ID_TYPE = '_get_id_type'
    PUSH_ID = '_push_id'
    PUSH_ID_ADDR = '_push_id_address'
    PUSH_NUM = '_push_num'
    PUSH_OPERATOR = '_push_operator'
    PUSH_INDEX = '_push_index'
    PUSH_SCOPE = '_push_scope'
    POP_SCOPE = '_pop_scope'
    DEFINE_VAR = '_define_variable'
    DEFINE_ARR = '_define_array'
    DEFINE_ARR_ARG = '_define_array_argument'
    START_PARAMS = '_start_params'
    CREATE_RECORD = '_create_record'
    NEW_RETURN = '_new_return'
    END_RETURN = '_end_return'
    NEW_BREAK = '_new_break'
    END_BREAK = '_end_break'
    BREAK_LOOP = '_break_loop'
    ITER_STMT = '_iteration_statement'
    RETURN_ANYWAY = '_return_anyway'
    CLEAN_UP = '_clean_up'
    SAVE = '_save'
    SAVE_RETURN = '_save_return'
    SAVE_OPERATION = '_save_operation'
    JPF_SAVE = '_jpf_save'
    JUMP = '_jump'
    JUMP_FILL_SAVE = '_jump_fill_save'
    ASSIGN_JUMP = '_assign_jump'
    ASSIGN_OPERATION = '_assign_operation'
    ARR_INDEX = '_array_index'
    MULT = '_multiply'
    NEGATE_FACTOR = '_negate_factor'
    IMPLICIT_OUTPUT = '_implicit_output'
    CALL_FUNC = '_call_function'
    FINISH_FUNC = '_finish_function'

class CodeGenerator:
    def __init__(self):
        self.SS = []
        self.PB = {}

    def call_routine(self, name, lookahead):
        self.__getattribute__(name)(lookahead)

    def _get_id_type(self, lookahead):
        pass

    def _push_id(self, lookahead):
        pass

    def _push_id_address(self, lookahead):
        pass

    def _push_num(self, lookahead):
        pass

    def _push_operator(self, lookahead):
        pass

    def _push_index(self, lookahead):
        pass

    def _push_scope(self, lookahead):
        pass

    def _pop_scope(self, lookahead):
        pass

    def _define_variable(self, lookahead):
        pass

    def _define_array(self, lookahead):
        pass

    def _define_array_argument(self, lookahead):
        pass

    def _start_params(self, lookahead):
        pass

    def _create_record(self, lookahead):
        pass

    def _new_return(self, lookahead):
        pass

    def _end_return(self, lookahead):
        pass

    def _new_break(self, lookahead):
        pass

    def _end_break(self, lookahead):
        pass

    def _break_loop(self, lookahead):
        pass

    def _iteration_statement(self, lookahead):
        pass

    def _return_anyway(self, lookahead):
        pass

    def _clean_up(self, lookahead):
        pass

    def _save(self, lookahead):
        pass

    def _save_return(self, lookahead):
        pass

    def _save_operation(self, lookahead):
        pass

    def _jpf_save(self, lookahead):
        pass

    def _jump(self, lookahead):
        pass

    def _jump_fill_save(self, lookahead):
        pass

    def _assign_jump(self, lookahead):
        pass

    def _assign_operation(self, lookahead):
        pass

    def _array_index(self, lookahead):
        pass

    def _multiply(self, lookahead):
        pass

    def _negate_factor(self, lookahead):
        pass

    def _implicit_output(self, lookahead):
        pass

    def _call_function(self, lookahead):
        pass

    def _finish_function(self, lookahead):
        pass
