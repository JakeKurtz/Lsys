from .util import extract_module

class LAxiom:
    def __init__(self, input_str):
        self.__string = ""
        self.__valid = self.__validate(input_str)

    def __validate(self, input_str):
        input_str = input_str.replace(" ", "")

        if input_str == "":
            print("LAxiom Error: the axiom cannot be empty.")
            return False

        success = True
        i = 0
        while i < len(input_str) and success:
            success, module, index_end = extract_module(input_str, i)
            i = index_end
            if (success):
                for p in module.parameters:
                    try:
                        float(p)
                    except ValueError:
                        print("LAxiom Error: the string \""+input_str+"\" is not a valid axiom. the parameter value \""+p+"\" is not a number.")
                        return False
            else:
                print("LAxiom Error: the string \""+input_str+"\" is not a valid axiom.")
                return False
        self.__string = input_str
        return True

    @property
    def string(self):
        return self.__string

    @property
    def valid(self):
        return self.__valid
