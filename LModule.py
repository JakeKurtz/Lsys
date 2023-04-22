import re

# ------------------------ Regular Expression Patterns ----------------------- #

re_func_name = r' *[A-Za-z]{1} *(\(|)'
re_input_struct = r'(.*(?::|).*)(=|\->)(.*(?::|))'
re_empty = r'( *|^$)'

re_valid_module_name = r'[+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}'

re_valid_module = r'^(?: *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *\( *([a-zA-Z_]+\w*(?: *, *[a-zA-Z_]+\w*)+|[a-zA-Z_]+\w*) *\) *| *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *|(^$))$'
re_valid_boolean = r'and|or|not|xor|<=|<|>|>=|!=|==|[<>!=]=|[<>]'
re_valid_math_expression = r'[ a-zA-Z0-9*+\-*\/%^]*'

re_test = r'(?: *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *\( *(.*(?: *, *.*)+|.*) *\) *| *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *|(^$))'

re_parameters = r'\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\)'
re_module = r'[A-Za-z]{1}(\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\)|)'

class LModule:

    def __init__(self, symbol, parameters):
        self.__symbol = symbol
        self.__parameters = parameters

    @property
    def symbol(self):
        return self.__symbol
    @property
    def parameters(self):
        return self.__parameters