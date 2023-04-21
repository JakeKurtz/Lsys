
def valid_expression(input_str):
    pass

class LParser:
    def __init__(self):
        pass
    def __del__(self):
        pass

    def add_var(self, name):
        self.__sym_dic[name] = 0

    def del_var(self, name):
        if self.__var_in_dic(name):
            del self.__sym_dic[name]
        else:
            print("Failed to delete variable. A variable with the name \""+ name + "\" does not exist.")

    def get_value(self, name):
        if self.__var_in_dic(name):
            return self.__sym_dic[name]
        else:
            return None

    def set_value(self, name, value):
        self.__sym_dic[name] = value

    def eval(self, input_str):
        pass

    def __var_in_dic(self, name):
        pass

    __sym_dic = {}