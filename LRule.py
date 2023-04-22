import re
import ast
from LModule import *
from LExpression import *

class LRule:

    def __init__(self, input_str):    
        self.__input = input_str

        pred_str = ""
        cond_str = ""
        succ_str = ""
        prob_raw = ""

        if match := re.match(re_input_struct, input_str):
            groups = match.groups()
            prefix = groups[0]
            suffix = groups[2]

            match = re.split(':', prefix)
            if len(match) == 2:
                pred_str, cond_str = match
            else:
                pred_str = prefix
                cond_str = "1"

            match = re.split(':', suffix)
            if len(match) == 2:
                succ_str, prob_raw = match
            else:
                succ_str = suffix
                prob_raw = "1"
            
        process_predecessor_string_success = self.__process_predecessor_string(pred_str)
        process_conditional_string_success = self.__process_conditional_string(cond_str)
        process_successor_string_success = self.__process_successor_string(succ_str)
        process_prob_string_success = self.__process_prob_string(prob_raw)

        self.__valid = (
            process_predecessor_string_success and
            process_conditional_string_success and
            process_successor_string_success and 
            process_prob_string_success
        )

    def __del__(self):
        pass

    def apply(self, left_context, symbol, right_context, replacement):
        pass

    @property
    def valid(self):
        return self.__valid
    @property
    def input_str(self):
        return self.__input_str

    __succ_modules = []

    __left_context = None
    __predecessor = None
    __right_context = None

    __condition = ""
    __prob = ""

    __valid = False
    
    __expr = LExpression()

    def __extract_parameters(self, input_str, i_offset):
        stack = 0
        i_start = None

        i = i_offset
        while i < len(input_str):
            c = input_str[i]
            if c == '(':
                if stack == 0:
                    i_start = i + 1
                stack += 1
            elif c == ')':
                stack -= 1
                if stack == 0:
                    return True, i, input_str[i_start:i]
            i+=1
        print("Brackets are not balenced you fucking twat!")
        return False, 0, ""

    def __extract_succ_modules(self, input_str):
        i = 0
        modules = []
        while i < len(input_str):
            c = input_str[i]
            if c != '(':
                valid_module_name = not (re.match(re_valid_module_name, c) == None)
                if input_str[(i+1) % (len(input_str))] == '(':
                    success, i, params = self.__extract_parameters(input_str, i)
                    if success and valid_module_name:
                        modules.append(LModule(c, params.split(',')))
                    else:
                        return False, []
                elif c == ')':
                    print("Brackets are not balenced you fucking twat!")
                    return False, []
                elif valid_module_name:
                    modules.append(LModule(c,[]))
            i+=1
        return True, modules

    def __extract_pred_module(self, input_str):
        input_str = input_str.replace(" ", "")
        symbol = ""
        parameters = []
        if match := re.match(re_valid_module, input_str):
            groups = [x for x in match.groups() if x != None]
            if len(groups) >= 1:
                symbol = groups[0]
            if len(groups) == 2:
                parameters = groups[1].split(',')
        else:
            print("LRule Error: Failed to varify production. \"" + input_str + "\" is not a valid module.")
            return False, None
        return True, LModule(symbol, parameters)

    def __process_predecessor_string(self, input_str):     
        left_context_str = ""
        pred_str = ""
        right_context_str = ""

        if match := re.search('(.*)<(.*)>(.*)', input_str):
            groups = match.groups()
            left_context_str = groups[0]
            pred_str = groups[1]
            right_context_str = groups[2]
        elif match := re.search('(.*)<(.*)', input_str):
            groups = match.groups()
            left_context_str = groups[0]
            pred_str = groups[1]
        elif match := re.search('(.*)>(.*)', input_str):
            groups = match.groups()
            pred_str = groups[0]
            right_context_str = groups[1]
        else:
            pred_str = input_str

        init_left_context_success, self.__left_context = self.__extract_pred_module(left_context_str)
        init_predecessor_success, self.__predecessor = self.__extract_pred_module(pred_str)
        init_right_context_success, self.__right_context = self.__extract_pred_module(right_context_str)

        if self.__predecessor.symbol == "":
            print("LRule Error: Failed to varify production. The predecessor cannot be an empty string.")
            init_predecessor_success = False

        init_variables_success = self.__init_variables()

        success = (
            init_left_context_success and 
            init_predecessor_success and 
            init_right_context_success and 
            init_variables_success )

        return success

    def __process_conditional_string(self, input_str):
        if re.match('^\s+|^$', input_str):
            condition = input_str.strip()
        else:
            condition = "1"

        if self.__expr.eval(condition) is not None:
            self.__condition = condition
            return True
        
        return False

    def __process_successor_string(self, input_str):
        init_successor_success, self.__succ_modules = self.__extract_succ_modules(input_str)
        return init_successor_success

    def __process_prob_string(self, input_str):
        input_str = input_str.strip(' ')
        if self.__expr.eval(input_str) is not None:
            self.__prob = input_str
            return True
        else:
            print("LRule Error: the production probability \"" + input_str + "\" can't be converted to a float." )
            return False

    def __init_variables(self):
        vars = []
        vars.extend(self.__left_context.parameters)
        vars.extend(self.__predecessor.parameters)
        vars.extend(self.__right_context.parameters)

        if len(set(vars)) == len(vars):
            for v in vars:
                self.__expr.add_var(v)
        else:
            print("LRule Error: Failed to initialize predecessor variables. Duplicates detected.")
            return False
        return True

rule = LRule("k(i,j,k) < A(m): m==(i+8) <= 10 = F(i,j,k,l,0)+F(i,j,k+5500*(imgay),l,1)+ : 1/100+50*0.5**10+o")
print(rule.valid)