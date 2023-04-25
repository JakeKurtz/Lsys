import re
from LModule import *

def extract_parameters(input_str, i_offset):
    stack = 0
    i_start = None

    i = i_offset
    while i < len(input_str):
        c = input_str[i]
        if c == '(':
            if stack == 0:
                i_start = i + 1
            stack += 1
        elif c == ')':
            stack -= 1
            if stack == 0:
                return True, i, input_str[i_start:i]
        i+=1
    print("Brackets are not balenced you fucking twat!")
    return False, 0, ""

def extract_module(input_str, i_offset=0):
    i = i_offset
    while i < len(input_str):
        c = input_str[i]
        if c != '(':
            valid_module_name = not (re.match(re_valid_module_name, c) == None)
            if input_str[(i+1) % (len(input_str))] == '(':
                success, i, params = extract_parameters(input_str, i)
                if success and valid_module_name:
                    return True, LModule(c, params.split(',')), i+1
                else:
                    break
            elif c == ')':
                break
            elif valid_module_name:
                return True, LModule(c), i+1
            else:
                break
        i+=1
    return False, None, i