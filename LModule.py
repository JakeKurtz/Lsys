import re

# ------------------------ Regular Expression Patterns ----------------------- #

re_func_name = ' *[A-Za-z]{1} *(\\(|)'
re_input_struct = '(.*(?::|).*)(=|\\->)(.*(?::|))'
re_empty = '( *|^$)'

re_valid_module = '^(?: *([A-Za-z]{1}) *\\( *([A-Za-z]+(?: *, *[A-Za-z]+)+|[A-Za-z]) *\\) *| *([A-Za-z]{1}) *|(^$))$'
re_valid_boolean = 'and|or|not|xor|<=|<|>|>=|!=|==|[<>!=]=|[<>]'
re_valid_math_expression = '[ a-zA-Z0-9*+\\-*\\/%^]*'

re_parameters = '\\((?:[^)(]+|\\((?:[^)(]+|\\([^)(]*\\))*\\))*\\)'
re_module = '[A-Za-z]{1}(\\((?:[^)(]+|\\((?:[^)(]+|\\([^)(]*\\))*\\))*\\)|)'

class LModule:

    def __init__(self, input_str):
        self.__symbol = input_str
        self.__parameters = []
        self.__valid = True
        
        if match := re.match(re_valid_module, input_str):
            groups = [x for x in match.groups() if x != None]

            if len(groups) >= 1:
                self.__symbol = groups[0]
            if len(groups) == 2:
                self.__parameters.extend(groups[1].split(','))
        else:
            self.__valid = False

    @property
    def valid(self):
        return self.__valid
    @property
    def symbol(self):
        return self.__symbol
    @property
    def parameters(self):
        return self.__parameters