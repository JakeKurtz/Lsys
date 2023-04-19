class LRule:

    def __init__(self, input_str):
        pass
    def __del__(self):
        pass

    def get_symbol(self):
        pass
    def get_input_string(self):
        pass
    def apply(self, left_context, symbol, right_context, replacement):
        pass
    def valid(self):
        pass

    @property
    def symbol(self):
        pass
    @property
    def input_str(self):
        pass

    @symbol.setter
    def symbol(self, value):
        pass
    @symbol.getter
    def symbol(self):
        pass

    @input_str.setter
    def input_str(self, value):
        pass
    @input_str.getter
    def input_str(self):
        pass

    __left_context = None
    __right_context = None

    __condition = ""
    __replacement = ""

    __variables = set()
    __replacement_parameters = {}

    __prob = 1.0

    __valid_symbols = False
    __valid_conditional = False
    __valid_replacement = False
    __valid_probability = False
    __valid_rule = False

    def __load_variables(self):
        pass

    def __process_symbol_string(self, input_str):
        pass
    def __process_conditional_string(self, input_str):
        pass
    def __process_replacement_string(self, input_str):
        pass

    def __verify_context(self, l_module, context_str):
        pass
    def __verify_symbol_context(self, l_context, r_context):
        pass

    def __process_prob_string(self, str):
        pass

    def __load_module_parameters(self, l_module, input_str):
        pass

    def __verify_symbols(self):
        pass

    def __valid_input_string(self, input_str):
        pass
