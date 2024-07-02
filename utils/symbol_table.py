class SymbolTable:
    def __init__(self, offset=0):
        self.offset = offset
        self.reset()

    def reset(self):
        self.symbol_table = [{}]

    def add_symbol(self, symbol, size=None, is_param=False):
        self.symbol_table[-1][symbol] = (self.offset, size, is_param)
        self.offset += 4 * size if size else 4
    
    def get_symbol(self, symbol):
        for entry in self.symbol_table[::-1]:
            if symbol in entry:
                return entry[symbol]
        return None

    def push_empty_stack(self):
        self.symbol_table.append({})
    
    def pop_stack(self):
        self.symbol_table.pop()