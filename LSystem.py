import time
import multiprocessing
import concurrent.futures
from math import ceil
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
    __generations = 5
    __max_nmb_threads = 100
    __nmb_threads = 1

    __foobar = []

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

    def __build_module_str(self, module):
        if len(module) > 1:
            return module[0] + "("+",".join(module[1].split(','))+")"
        else:
            return module[0]

    def __thread_func_test(self, id, symbols):
        strings = [''] * len(symbols)
        for i, sym in enumerate(symbols):

            l_context = symbols[i-1] if i-1 >= 0 else ()
            pred = sym
            r_context = symbols[i+1] if i+1 < len(symbols) else ()
            
            strings[i] = self.__build_module_str(pred)

            if pred[0] in self.__rule_dic:
                rules = self.__rule_dic[pred[0]]
                for r in rules:
                    strings[i] = r.apply(l_context, pred, r_context)
        if (self.__nmb_threads == 1):
            self.__foobar[id] = "".join(strings) 
        elif (id == 0):
            self.__foobar[id] = "".join(strings[:-1]) 
        elif (id == (self.__nmb_threads-1)):
            self.__foobar[id] = "".join(strings[1:])
        else:
            self.__foobar[id] = "".join(strings[1:-1])


    def generate(self):

        self.__string = self.__axiom.string
        regex_comp = re.compile(re_valid_module)

        for gen in range(self.__generations):
            symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(self.__string)]
            #strings = [''] * len(self.__string)

            # ----------------------- Partition symbols into chunks ---------------------- #
            # This code sucks major balls
            nmb_threads = self.__max_nmb_threads
            nmb_symbols = len(symbols)

            if (nmb_symbols <= nmb_threads or nmb_threads == 1):
                symbol_chunks = [symbols]
            else:
                while(True):
                    n = int(ceil(nmb_symbols / nmb_threads))
                    if (n-2 > 0):
                        break
                    else:
                        pass

            if (len(symbols) < nmb_threads or nmb_threads == 1):
                symbol_chunks = [symbols]
            else:
                n = 0
                while (True):
                    n = int(ceil(len(symbols) / nmb_threads))
                    if (n-2 > 0):
                        break
                    nmb_threads -= 1

                symbol_chunks = [symbols[i:i+n] for i in range(0, len(symbols)-2, n-2)] if len(symbols) > 1 else [symbols]
            self.__nmb_threads = len(symbol_chunks)
            self.__foobar = [''] * self.__nmb_threads

            print(self.__nmb_threads)

            #for i, chunk in enumerate(symbol_chunks):
            #    print("list_"+str(i)+": ", chunk)
            #print("\n")

            # ---------------------------------------------------------------------------- #
            '''
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
            '''

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.__nmb_threads) as executor:
                executor.map(self.__thread_func_test, range(self.__nmb_threads), symbol_chunks)

            #print(self.__foobar)
            self.__string = "".join(self.__foobar)
            #print("gen_"+str(gen)+": "+self.__string)

lsys = Lsystem()

lsys.set_axiom(LAxiom("F"))
lsys.add_rule(LRule("F -> F[+F]F[-F][F]"))

#lsys.set_axiom(LAxiom("baAAA"))
#lsys.add_rule(LRule("b -> a"))
#lsys.add_rule(LRule("b < a -> b"))

start = time.time()
lsys.generate()
end = time.time()
print(len(lsys.string), end - start)

