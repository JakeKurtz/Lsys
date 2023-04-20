import re

# ------------------------ Regular Expression Patterns ----------------------- #

re_func_name = ' *[A-Za-z]{1} *(\\(|)'
re_input_struct = '(.*(?::|).*)(=|\\->)(.*(?::|))'
re_empty = '( *|^$)'

re_valid_module = '( *[A-Za-z]{1} *\\( *([A-Za-z]+(?: *, *[A-Za-z]+)+|[A-Za-z]) *\\) *| *[A-Za-z]{1} *)|^$'
re_valid_boolean = 'and|or|not|xor|<=|<|>|>=|!=|==|[<>!=]=|[<>]'
re_valid_math_expression = '[ a-zA-Z0-9*+\\-*\\/%^]*'

re_parameters = '\\((?:[^)(]+|\\((?:[^)(]+|\\([^)(]*\\))*\\))*\\)'
re_module = '[A-Za-z]{1}(\\((?:[^)(]+|\\((?:[^)(]+|\\([^)(]*\\))*\\))*\\)|)'

class LModule:

    def __init__(self, input_str):
        self.__symbol = ""
        self.__parameters = []
        
        match = re.match(re_valid_module, input_str)
        if match:
            self.__extract_symbol(input_str)
            self.__extract_parameters(input_str)
            self.__valid = True
        else:
            self.__symbol = input_str
            self.__valid = False

    def __extract_symbol(self, input_str):
        match = re.search(re_func_name, input_str)
        if match:
            self.__symbol = re.sub('[() ]', '', match[0])

    def __extract_parameters(self, input_str):
        match = re.search(re_parameters, input_str)
        if match:
            parameters_raw = re.sub('[()]', '', match[0])
            parameters = parameters_raw.split(',')
            self.__parameters.extend(parameters)
            match = re.search(re_parameters, input_str)

    @property
    def valid(self):
        return self.__valid
    @property
    def symbol(self):
        return self.__symbol
    @property
    def parameters(self):
        return self.__parameters