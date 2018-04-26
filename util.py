## file for smaller and general functions
import p2336 as p2

def is_operator(s):
    return s in ["+", "-", "/", "*", "^", "%", "=", ">", "<", "!=", "(", ")"]


# check to see a given string, s, is a reserved word
def is_reserved(s):
    return s in ["get", "output", "goto", "stop", "let", "if"]


def check_expression(string):
    for i in string:
        if is_operator(i):
            return True
    return False


def make_two_digit(number):
    if not len(number) == 1:
        return str(number)
    else:
        return "0" + str(number)


def return_iml_code(var):
    code = {
        "get": "12",
        "read": "12",
        "output": "11",
        "write": "11",
        "goto": "41",
        "branch": "41",
        "load": "22",
        "store": "21",
        "add": "31",
        "subtract": "32",
        "multiply": "33",
        "divide": "34",
        "branchzero": "42",
        "branchpos": "43",
        "stop": "990000",
        "halt": "990000"
    }
    return code[var]


def ops_to_string(ops):
    ops_to_string = {
        "+": "add",
        "-": "subtract",
        "*": "multiply",
        "/": "divide",
    }
    return ops_to_string[ops]


def tokenizer(content):
    tokens = []

    content_by_line = content.split("\n")
    for line in content_by_line:
        # print(line)
        array_code = line.split(" ")
        for i in array_code:
            if i == "cmt":
                tokens.append(i)
                break
            tokens.append(i)
    return tokens


def make_symbol_table(content):
    min_mem = 0
    max_mem = 99

    table = []
    dup = []

    mem_dict ={}

    content_by_line = content.split("\n")
    for line in content_by_line:
        array_code = line.split(" ")
        for i in array_code:
            if i not in dup:
                if i == "goto" or i == "cmt":
                    break
                if array_code.index(i) == 0:
                    table.append(["L", array_code[0], min_mem])
                    min_mem += 1
                elif not (is_operator(i)) and not (is_reserved(i)):
                    if i.isdigit():
                        table.append(["C", i, max_mem])
                        mem_dict[i] = max_mem
                        max_mem -= 1
                    elif i.isalpha() or i.isalnum():
                        table.append(["V", i, max_mem])
                        mem_dict[i] = max_mem
                        max_mem -= 1
                    dup.append(i)
    return table, mem_dict


def get_statement(line, mem_dict, array_code, ln):
    line_split = line.split(" ")
    iml_code = return_iml_code("get") + make_two_digit(str(mem_dict[line_split[-1]])) + "00"
    array_code[ln] = iml_code
    ln += 1
    return array_code, ln


def is_expression(string):
    ops = ["+", "-", "/", "*", "^", "%"]
    for i in ops:
        if i in string:
            return True
    return False


def get_expression(line):
    exp = ""
    line_split = line.split(" ")
    for word in line_split:
        if not word == "let":
            exp += word
    return exp[4:len(exp)]

register = {"01": False, "02": False, "03": False, "04": False}


def get_registration():
    # register = {"01": False, "02": False, "03": False, "04": False}
    for reg, val in register.items():
        if not val:
            register[reg] = True
            return reg
    if register["04"]:
        return list(register.keys())[0]


def let_statement(line, mem_dict, array_code, ln):
    exp = get_expression(line)
    if is_expression(exp):
        postfix = p2.infixToPostfix(exp)
        code = p2.postfixEval(postfix, mem_dict)
        code_split = code.split("\n")
        for i in code_split:
            array_code[ln] = i
            ln += 1
    else:
        exp_str = str(exp)
        array_code[ln] = return_iml_code("load") + get_registration() + str(mem_dict[exp_str])
        ln += 1
    return array_code, ln



