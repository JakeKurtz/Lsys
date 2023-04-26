import time
from multiprocessing import Pool, freeze_support
from functools import partial
from LRule import *
from LAxiom import *
from util import re_valid_module

class Lsystem:
    def __init__(self):
        pass

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
    __symbols = []
    __generations = 15
    __nmb_threads = 2

    def __build_module_str(self, module):
        if len(module) > 1:
            return module[0] + "("+",".join(module[1].split(','))+")"
        else:
            return module[0]

    def _thread_func_test(self, i, sym, rule_dic):
        l_context = self.__symbols[i-1] if i-1 >= 0 else ()
        pred = sym
        r_context = self.__symbols[i+1] if i+1 < len(self.__symbols) else ()

        string = self.__build_module_str(pred)

        if pred[0] in rule_dic:
            rules = rule_dic[pred[0]]
            for r in rules:
                string = r.apply(l_context, pred, r_context)
        return string

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

    def generate(self):
        pool = Pool(self.__nmb_threads)
        self.__string = self.__axiom.string
        regex_comp = re.compile(re_valid_module)

        start = time.time()
        for gen in range(self.__generations):
            self.__symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(self.__string)]

            results = pool.starmap(partial(self._thread_func_test, rule_dic=self.__rule_dic), (enumerate(self.__symbols)))
            #results = pool.starmap(self._thread_func_test, enumerate(self.__symbols))
            self.__string = "".join(results)

            #print(self.__string)

        end = time.time()
        print(len(self.__string), end - start)
        pool.close()

if __name__ == '__main__':
    freeze_support()  # needed for Windows

    lsys = Lsystem()

    #lsys.set_axiom(LAxiom("X(1,2)"))
    #lsys.add_rule(LRule("X(i,j)=F[-X(i*2,j/2)][+X(j,i)]"))

    lsys.set_axiom(LAxiom("X"))
    lsys.add_rule(LRule("X=F[-X][+X]"))

    #lsys.set_axiom(LAxiom("baaaaaaa"))
    #lsys.add_rule(LRule("b -> a"))
    #lsys.add_rule(LRule("b < a -> b"))

    lsys.generate()

