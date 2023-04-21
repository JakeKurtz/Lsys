import re
import ast
from LModule import *

class LRule:

    def __init__(self, input_str):
        
        self.__input = input_str

        sym_raw = ""
        condition_raw = ""
        replacement_raw = ""
        prob_raw = ""

        match = re.match(re_input_struct, input_str)
        if match:
            groups = match.groups()
            prefix = groups[0]
            suffix = groups[2]

            match = re.split(':', prefix)
            if len(match) == 2:
                sym_raw, condition_raw = match
            else:
                sym_raw = prefix
                condition_raw = "1"

            match = re.split(':', suffix)
            if len(match) == 2:
                replacement_raw, prob_raw = match
            else:
                replacement_raw = suffix
                prob_raw = "1"
            
        self.__process_symbol_string(sym_raw)
        self.__process_conditional_string(condition_raw)
        #self.__process_replacement_string(replacement_raw)
        self.__process_prob_string(prob_raw)

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
    def left_context(self):
        return self.__left_context
    @property
    def symbol(self):
        return self.__symbol
    @property
    def right_context(self):
        return self.__right_context
    @property
    def input_str(self):
        return self.__input_str

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
        
        left_context_str = ""
        sym_str = ""
        right_context_str = ""

        if match := re.search('(.*)<(.*)>(.*)', input_str):
            groups = match.groups()
            left_context_str = groups[0]
            sym_str = groups[1]
            right_context_str = groups[2]
        elif match := re.search('(.*)<(.*)', input_str):
            groups = match.groups()
            left_context_str = groups[0]
            sym_str = groups[1]
        elif match := re.search('(.*)>(.*)', input_str):
            groups = match.groups()
            sym_str = groups[0]
            right_context_str = groups[1]
        else:
            sym_str = input_str

        left_context_str = left_context_str.replace(" ", "")
        sym_str = sym_str.replace(" ", "")
        right_context_str = right_context_str.replace(" ", "")

        self.__left_context = LModule(left_context_str)
        self.__symbol = LModule(sym_str)
        self.__right_context = LModule(right_context_str)

        self.__verify_symbols()

    def __process_conditional_string(self, input_str):
        if re.match('^\s+|^$', input_str):
            condition = input_str.strip()
        else:
            condition = "1"
        try:
            ast.parse(condition)
            self.__valid_conditional = True
        except SyntaxError:
            print("LRule Error: parser failed to compile. The conditional expression \"" + condition +"\" is invalid.")
        
        print(condition)

    def __process_replacement_string(self, input_str):
        suffix = ""
        prefix = ""

        input_str = input_str.replace(" ", "")

        self.__valid_replacement = True
        while match := re.search(re_parameters, input_str) and self.__valid_replacement:
            parameters_raw = match[0].strip('()')
            parameters = parameters_raw.split(',')

    def __process_prob_string(self, input_str):
        input_str = input_str.strip(' ')
        try:
            parse = ast.parse(input_str, mode="eval")

            valid_expression = True
            for node in ast.walk(parse):
                if not isinstance(node, (ast.Constant, ast.Expression, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)):
                    valid_expression = False
                    break
                    
            if valid_expression:
                prob = float(eval(compile(parse, "<string>", "eval")))
                print(prob)
                if (prob > 1.0 or prob < 0.0):
                    print("LRule Error: the production probability \"" + input_str + "\" is outside the range [0, 1].")
                else:
                    self.__prob = prob
            else:
                print("LRule Error: the production probability \"" + input_str + "\" can't be converted to a float." )

        except ValueError:
            print("LRule Error: the production probability \"" + input_str + "\" can't be converted to a float." )

    def __verify_context(self, l_module, context_str):
        pass
    
    def __verify_symbol_context(self, l_context, r_context):
        pass

    def __load_module_parameters(self, l_module, input_str):
        pass

    def __verify_symbols(self):
        valid = True
        if not self.__left_context.valid:
            print("LRule Error: Failed to varify production. The left context \"" + self.__left_context.symbol + "\" is not a valid module.")
            valid = False
        if not self.__symbol.valid:
            print("LRule Error: Failed to varify production. The symbol \"" + self.__symbol.symbol + "\" is not a valid module.")
            valid = False
        if self.__symbol.symbol == "":
            print("LRule Error: Failed to varify production. The Symbol cannot be an empty string.")
            valid = False
        if not self.__right_context.valid:
            print("LRule Error: Failed to varify production. The right context \"" + self.__right_context.symbol + "\" is not a valid module.")
            valid = False
        return valid

    def __valid_input_string(self, input_str):
        pass


rule = LRule("H(i,j,k) < A(a,b,c) > C: m==0 = F(i,j,k,l,0)+F(i,j,k,l,1)+ : 1/100+50*0.5**10")