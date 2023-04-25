from dataclasses import dataclass, field
from typing import List
# ------------------------ Regular Expression Patterns ----------------------- #

re_func_name = r' *[A-Za-z]{1} *(\(|)'
re_input_struct = r'(.*(?::|).*)(=|\->)(.*(?::|))'
re_empty = r'( *|^$)'

re_valid_module_name = r'[+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}'

re_valid_number = r'(?=.)(?:[+-]?(?:[0-9]*)(?:\.(?:[0-9]+))?)'

re_valid_module = r'^(?: *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *\( *([a-zA-Z_]+\w*(?: *, *[a-zA-Z_]+\w*)+|[a-zA-Z_]+\w*) *\) *| *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *|(^$))$'

re_valid_module_2 = r'(?: *('+re_valid_module_name+r') *\( *('+re_valid_number+r'(?: *, *'+re_valid_number+r')+|'+re_valid_number+r') *\) *| *('+re_valid_module_name+r') *)'

re_valid_boolean = r'and|or|not|xor|<=|<|>|>=|!=|==|[<>!=]=|[<>]'
re_valid_math_expression = r'[ a-zA-Z0-9*+\-*\/%^]*'
re_valid_parameter_name = r'^[a-zA-Z_]\w*$'

re_test = r'(?: *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *\( *(.*(?: *, *.*)+|.*) *\) *| *([+\-&^\\\/|*~\"!;_?@\'#%$\[\].\{\}a-zA-Z]{1}) *|(^$))'

re_parameters = r'\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\)'
re_module = r'[A-Za-z]{1}(\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\)|)'

@dataclass
class LModule:
    symbol: str = ''
    parameters: List[str] = field(default_factory=list)

    '''
    def __init__(self, symbol="", parameters=[]):
        self.__symbol = symbol
        self.__parameters = parameters

    @property
    def symbol(self):
        return self.__symbol
    @property
    def parameters(self):
        return self.__parameters
    '''