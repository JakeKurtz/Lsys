import time
from multiprocessing import Pool, freeze_support

from LRule import *
from LAxiom import *
from util import re_valid_module, valid_commands

def chunks(l, n):
    """Yield n number of sequential chunks from l."""
    d, r = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]

def init_processes(rule_instance):
    """
    Initialize each process in the process pool with global variable rules.
    """
    global rules
    rules = rule_instance

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
    __generations = 8
    __nmb_threads = 12

    def __build_module_str(self, module):
        if len(module) > 1:
            return module[0] + "("+",".join(module[1].split(','))+")"
        else:
            return module[0]

    def _process_symbols(self, symbols):
        l_context, pred, r_context = symbols
        string = self.__build_module_str(pred)
        if pred[0] in rules:
            rule_sym = rules[pred[0]]
            for rule in rule_sym:
                string = rule.apply(l_context, pred, r_context)
        return string

    def __process_symbols(self, symbols):
        l_context, pred, r_context = symbols
        string = self.__build_module_str(pred)
        if pred[0] in self.__rule_dic:
            rule_sym = self.__rule_dic[pred[0]]
            for rule in rule_sym:
                string = rule.apply(l_context, pred, r_context)
        return string

    def _process_symbol_chunk(self, sym_chunk):
        results = [''] * len(sym_chunk)
        for i, sym in enumerate(sym_chunk):
            results[i] = self._process_symbols(sym)
        return "".join(results)

    def __process_input_string(self, regex_comp, input_str):
        symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(input_str)]

        nmb_symbols = len(symbols)
        symbol_chunks = [[]] * nmb_symbols

        if nmb_symbols == 1:
            symbol_chunks[0] = [[],symbols[0],[]]
        else:
            symbol_chunks[0] = [[]]
            symbol_chunks[0].extend(symbols[0:2])

            for i in range(1, nmb_symbols):
                if i == (nmb_symbols-1):
                    symbol_chunks[i] = symbols[i-1:nmb_symbols]
                    symbol_chunks[i].insert(2, [])
                else:
                    symbol_chunks[i] = symbols[i-1:i+2]
        return symbol_chunks

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
        pool = Pool(processes=self.__nmb_threads, initializer=init_processes, initargs=(self.__rule_dic,))
        self.__string = self.__axiom.string
        regex_comp = re.compile(re_valid_module)

        start = time.time()
        for gen in range(self.__generations):

            symbols = self.__process_input_string(regex_comp, self.__string)

            # ------------------------------- Multiprocess ------------------------------- #
            
            symbol_chunks = chunks(symbols, self.__nmb_threads*5)
            results = pool.map(self._process_symbol_chunk, symbol_chunks)

            # ----------------------------------- Loop ----------------------------------- #

            #results = [''] * len(symbols)
            #for i, sym in enumerate(symbols):
            #    results[i] = self.__process_symbols(sym)

            # ---------------------------------------------------------------------------- #

            self.__string = "".join(results)
            #print(self.__string)

        symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(self.__string)]
        command_list = [None] * len(symbols)
        for i, sym in enumerate(symbols):
            if sym[0] in valid_commands:
                s = sym[0]
                p = sym[1] if len(sym) > 1 else []
                command_list[i] = LModule(s, p)

        print("string size:"+str(len(self.__string)), "\nnmb of commands = "+str(len(command_list)))

        end = time.time()
        print(len(self.__string), "took: "+str(end - start)+"s\n")
        pool.close()

if __name__ == '__main__':
    freeze_support()  # needed for Windows

    lsys = Lsystem()

    lsys.set_axiom(LAxiom("X(1,2)"))
    lsys.add_rule(LRule("X(i,j)=F[-X(i*2,j/2)][+X(j,i)]"))

    #lsys.set_axiom(LAxiom("X"))
    #lsys.add_rule(LRule("X=F[-X][+X]"))

    #lsys.set_axiom(LAxiom("baaaaaaa"))
    #lsys.add_rule(LRule("b -> a"))
    #lsys.add_rule(LRule("b < a -> b"))

    lsys.generate()

