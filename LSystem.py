class Lsystem:

    def __init__(self):
        pass
    def __del__(self):
        pass

    def add_rule(self, rule):
        pass
    def del_rule(self, sym, index):
        pass

    @property
    def axiom(self):
        pass
    @property
    def generations(self):
        pass

    @axiom.setter
    def axiom(self, value):
        pass
    @axiom.getter
    def axiom(self):
        pass

    @generations.setter
    def generations(self, value):
        pass
    @generations.getter
    def generations(self):
        pass

    __l_system = ""
    __rules = {}

    def __generate(self):
        pass

    def __get_symbol_range(self, input_str, start_pos, end_pos):
        pass
    