import time
from LRule import *
from LAxiom import *
from util import extract_module

class Lsystem:

    def __init__(self):
        pass
    def __del__(self):
        pass

    def add_rule(self, rule):
        if rule.symbol in self.__rule_dic:
            self.__rule_dic[rule.symbol].append(rule)
        else:
            self.__rule_dic[rule.symbol] = [rule]

    def del_rule(self, sym):
        if sym in self.__rule_dic:
            del self.__rule_dic[sym]
        else:
            print("Failed to delete rule. A rule with the symbol \""+ sym + "\" does not exist.")

    @property
    def string(self):
        return self.__string

    def set_axiom(self, value):
        self.__axiom = value

    @property
    def generations(self):
        return self.__generations
    @generations.setter
    def generations(self, value):
        self.__generations = value

    __axiom = None
    __string = ""
    __rule_dic = {}
    __generations = 9

    def __build_module_str(self, module):
        if len(module) > 1:
            return module[0] + "("+",".join(module[1].split(','))+")"
        else:
            return module[0]

    def generate(self):

        self.__string = self.__axiom.string
        regex_comp = re.compile(re_valid_module_2)

        for gen in range(self.__generations):
            symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(self.__string)]
            strings = [''] * len(self.__string)
            for i, sym in enumerate(symbols):

                l_context = symbols[i-1] if i-1 >= 0 else ()
                pred = sym
                r_context = symbols[i+1] if i+1 < len(symbols) else ()
                
                strings[i] = self.__build_module_str(pred)

                if pred[0] in self.__rule_dic:
                    rules = self.__rule_dic[pred[0]]
                    for r in rules:
                        strings[i] = r.apply(l_context, pred, r_context)

            self.__string = "".join(strings)
            #print("gen_"+str(gen)+": "+self.__string)

lsys = Lsystem()

lsys.set_axiom(LAxiom("F"))
lsys.add_rule(LRule("F -> F[+F]F[-F][F]"))

#lsys.set_axiom(LAxiom("baaaaaaaa"))
#lsys.add_rule(LRule("b -> a"))
#lsys.add_rule(LRule("b < a -> b"))

start = time.time()
lsys.generate()
end = time.time()
print(len(lsys.string), end - start)

regex_comp = re.compile(re_valid_module_2)

