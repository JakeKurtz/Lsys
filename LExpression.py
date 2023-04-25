import ast
import random
import operator as op

def valid_expression(input_str):
    pass

class LExpression:

    def add_var(self, name):
        self.__sym_dic[name] = random.uniform(0, 1)

    def del_var(self, name):
        if name in self.__sym_dic:
            del self.__sym_dic[name]
        else:
            print("Failed to delete variable. A variable with the name \""+ name + "\" does not exist.")

    def get_value(self, name):
        if name in self.__sym_dic:
            return self.__sym_dic[name]
        else:
            print("Failed to get variable. A variable with the name \""+ name + "\" does not exist.")
            return None

    def set_value(self, name, value):
        self.__sym_dic[name] = value

    def __eval(self, node):
        if isinstance(node, ast.Num): # <number>
            return node.n
        elif isinstance(node, ast.BinOp): # <left> <operator> <right>
            return self.__sym_dic[type(node.op)](self.__eval(node.left), self.__eval(node.right))
        elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
            return self.__sym_dic[type(node.op)](self.__eval(node.operand))
        elif isinstance(node, ast.Compare):
            compare_out = True
            for i, op in enumerate(node.ops):
                compare_out = compare_out and self.__sym_dic[type(op)](self.__eval(node.left), self.__eval(node.comparators[i]))
                node.left = node.comparators[i]
            return compare_out
        elif isinstance(node, ast.Name):
            if node.id not in self.__sym_dic:
                print("LExpression Error: the symbol \""+str(node.id)+"\" is unknown.")
                raise TypeError(node)
            else:
                return self.__sym_dic[node.id]
        else:
            raise TypeError(node)

    def parse(self, input_str):
        try:
            node = ast.parse(input_str, mode="eval")
            for n in ast.walk(node):
                if not isinstance(n, self.__op_white_list):
                    return None
            return node
        except SyntaxError:
            return None

    def eval(self, input_str):
        if node := self.parse(input_str):
            try:
                return self.__eval(node.body)
            except TypeError as e:
                return None
            except ZeroDivisionError as e:
                return None
        else:
            return None

    __sym_dic = {
        ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, 
        ast.Pow: op.pow, ast.USub: op.neg, ast.Eq: op.eq, ast.NotEq: op.ne, ast.Lt: op.lt, ast.LtE: op.le }

    __op_white_list = (
        ast.Compare,    ast.Eq,     ast.NotEq,  ast.Lt, 
        ast.LtE,        ast.Gt,     ast.GtE,    ast.Is, 
        ast.IsNot,      ast.Load,   ast.Name,   ast.Constant, 
        ast.Expression, ast.BinOp,  ast.Add,    ast.Sub, 
        ast.Mult,       ast.Div,    ast.Pow,    ast.Mod,
        ast.BoolOp,     ast.Not)