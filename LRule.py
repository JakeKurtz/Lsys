import re
from .util import extract_module, re_input_struct, re_valid_parameter_name
from .LModule import LModule
from .LExpression import LExpression

class LRule:

    def __init__(self, input_str):    
        self.__input = input_str
        self.__valid = False
        self.__expr = LExpression()

        self.__l_context = LModule()
        self.__pred = LModule()
        self.__r_context = LModule()

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
            
        if self.__process_predecessor_string(pred_str):
            if self.__process_conditional_string(cond_str):
                if self.__process_successor_string(succ_str):
                    if self.__process_prob_string(prob_raw):
                         self.__valid = True

    def apply(self, lc, pred, rc):
        _lc = self.__valid_module(self.__l_context,   lc) 
        _pred = self.__valid_module(self.__pred,      pred) 
        _rc = self.__valid_module(self.__r_context,   rc)

        if (_lc != None and _pred != None and _rc != None):
            self.__load_module_parameters(self.__l_context, _lc)
            self.__load_module_parameters(self.__pred,      _pred)
            self.__load_module_parameters(self.__r_context, _rc)
            if (self.__condition == "1" or self.__expr.eval(self.__condition)):
                return ''.join([self.__build_module_str(module) for module in self.__succ_modules])

        if len(pred) > 1:
            output = "".join((pred[0],"(",pred[1],")"))
        else:
            output = pred[0]
        return output

    @property
    def valid(self):
        return self.__valid
    @property
    def input_str(self):
        return self.__input_str
    @property
    def symbol(self):
        return self.__pred.symbol

    __succ_modules = []

    __l_context = None
    __pred = None
    __r_context = None

    __condition = ""
    __prob = ""

    __valid = False
    __expr = None

    def __build_module_str(self, module):
        if len(module.parameters) != 0:
            eval_params = [str(self.__expr.eval(p)) for p in module.parameters]
            return module.symbol + "("+",".join(eval_params)+")"
        else:
            return module.symbol

    def __valid_module(self, module_dom, module_sub):
        if module_dom.symbol == '':
            return module_dom
        else:
            symbol = module_sub[0] if len(module_sub) > 0 else ''
            parameters = module_sub[1].split(',') if len(module_sub) > 1 else []

            valid_symbol = (module_dom.symbol == symbol)
            valid_parameter_list = (len(module_dom.parameters) == len(parameters))

            if (valid_symbol and valid_parameter_list):
                return LModule(symbol, parameters)
            else:
                return None

    def __load_module_parameters(self, module_dom, module_sub):
        for i in range(len(module_dom.parameters)):
            sym = module_dom.parameters[i]
            val = module_sub.parameters[i]
            self.__expr.set_value(sym, float(val))

    def __process_predecessor_string(self, input_str):
        success = True

        l_context_str = ""
        pred_str = ""
        r_context_str = ""

        input_str = input_str.replace(" ", "")

        if match := re.search('(.*)<(.*)>(.*)', input_str):
            groups = match.groups()
            l_context_str = groups[0]
            pred_str = groups[1]
            r_context_str = groups[2]
        elif match := re.search('(.*)<(.*)', input_str):
            groups = match.groups()
            l_context_str = groups[0]
            pred_str = groups[1]
        elif match := re.search('(.*)>(.*)', input_str):
            groups = match.groups()
            pred_str = groups[0]
            r_context_str = groups[1]
        else:
            pred_str = input_str

        if l_context_str != "":
            modules_success, self.__l_context, index_end = extract_module(l_context_str)
            if not modules_success:
                print("LRule Error: Failed to extract left context. \""+l_context_str+"\" is not a valid module.")
                success = False

        modules_success, self.__pred, index_end = extract_module(pred_str)
        if not modules_success:
            print("LRule Error: Failed to extract predecessor. \""+pred_str+"\" is not a valid module.")
            success = False
        elif self.__pred.symbol == "":
            print("LRule Error: Failed to varify production. The predecessor cannot be empty.")
            success = False

        if r_context_str != "":
            modules_success, self.__r_context, index_end = extract_module(r_context_str)
            if not modules_success:
                print("LRule Error: Failed to extract right context. \""+r_context_str+"\" is not a valid module.")
                success = False

        if success: 
            success = self.__init_variables()

        return success

    def __process_conditional_string(self, input_str):
        if re.match('^\s+|^$', input_str):
            condition = input_str.strip()
        else:
            condition = "1"

        if self.__expr.eval(condition) is not None:
            self.__condition = condition
            return True
        
        print("LRule Error: conditional failed to evaluate.")
        return False

    def __process_successor_string(self, input_str):
        input_str = input_str.replace(" ", "")
        modules = []
        success = True
        i = 0
        while i < len(input_str) and success:
            success, module, index_end = extract_module(input_str, i)
            i = index_end
            if (success):
                for expr in module.parameters:
                    if self.__expr.eval(expr) is None:
                        print("LRule: the parameter expression \""+expr+"\" failed to evaluate.")
                        return False
                modules.append(module)
            else:
                return False
        self.__succ_modules = modules
        return True

    def __process_prob_string(self, input_str):
        input_str = input_str.replace(" ", "")
        if self.__expr.eval(input_str) is not None:
            self.__prob = input_str
            return True
        else:
            print("LRule: the probability expression \""+input_str+"\" failed to evaluate.")
            return False

    def __init_variables(self):
        vars = []
        vars.extend(self.__l_context.parameters)
        vars.extend(self.__pred.parameters)
        vars.extend(self.__r_context.parameters)

        if len(set(vars)) == len(vars):
            for v in vars:
                if (re.match(re_valid_parameter_name, v)):
                    self.__expr.add_var(v)
                    print(self.__expr)
                else:
                    print("LRule Error: The variable name \""+v+"\" is not valid. A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ ) and cannot start with a number.")
                    return False
        else:
            print("LRule Error: Failed to initialize predecessor variables. Duplicates detected.")
            return False
        return True