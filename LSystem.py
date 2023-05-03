import re
import time
#from multiprocessing import Pool

from .util import re_valid_module, valid_commands
from .LModule import LModule

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
        print("Created a new Lsystem!")
        self.__command_list = []

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

    @property
    def command_list(self):
        return self.__command_list

    __axiom = None
    __string = ""

    __rules = {}
    __rule_bookkeep = {}

    __generations = 10
    __nmb_threads = 12

    def __build_module_str(self, module):
        if len(module) > 1:
            return module[0] + "("+",".join(module[1].split(','))+")"
        else:
            return module[0]

    def __process_symbols(self, symbols):
        l_context, pred, r_context = symbols

        string = self.__build_module_str(pred)

        pred_sym = pred[0]
        if pred_sym in self.__rules:
            rules = self.__rules[pred_sym]
            for r in rules:
                string = r.apply(l_context, pred, r_context)
                
        return string

    def _process_symbol_chunk(self, sym_chunk):
        results = [''] * len(sym_chunk)
        for i, sym in enumerate(sym_chunk):
            results[i] = self.__process_symbols(sym)
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

    def axiom_valid(self):
        return self.__axiom.valid

    def rule_valid(self, key):
        if key in self.__rule_bookkeep:
            return self.__rule_bookkeep[key].valid
        return False

    def add_rule(self, key, rule):
        self.del_rule(key)
        self.__rule_bookkeep[key] = rule

    def del_rule(self, key):
        if key in self.__rule_bookkeep:
            del self.__rule_bookkeep[key]

    def generate(self):
        # build rule dic
        self.__rules.clear()
        for rule in self.__rule_bookkeep.values():
            sym = rule.symbol
            if sym in self.__rules:
                self.__rules[sym].append(rule)
            else:
                self.__rules[sym] = [rule]

        #pool = Pool(processes=self.__nmb_threads, initializer=init_processes, initargs=(self.__rules,))
        self.__string = self.__axiom.string
        regex_comp = re.compile(re_valid_module)

        #start = time.time()
        for gen in range(self.__generations):

            symbols = self.__process_input_string(regex_comp, self.__string)

            # ------------------------------- Multiprocess ------------------------------- #
            
            #symbol_chunks = chunks(symbols, self.__nmb_threads*5)
            #results = pool.map(self._process_symbol_chunk, symbol_chunks)

            # ----------------------------------- Loop ----------------------------------- #

            results = [''] * len(symbols)
            for i, sym in enumerate(symbols):
                results[i] = self.__process_symbols(sym)

            # ---------------------------------------------------------------------------- #

            self.__string = "".join(results)
            #print(self.__string)

        symbols = [[sym for sym in group if sym != ''] for group in regex_comp.findall(self.__string)]
        self.__command_list = [None] * len(symbols)
        for i, sym in enumerate(symbols):
            if sym[0] in valid_commands:
                s = sym[0]
                p = [float(x) for x in sym[1].split(',')] if len(sym) > 1 else []
                self.__command_list[i] = LModule(s, p)
        self.__command_list = list(filter(lambda item: item is not None, self.__command_list))

        #print("string size:"+str(len(self.__string)), "\nnmb of commands = "+str(len(command_list)))

        #end = time.time()
        #print(len(self.__string), "took: "+str(end - start)+"s\n")
        #pool.close()