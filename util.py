# file for smaller and general functions
import p2336 as p2

register = {"01": False, "02": False, "03": False, "04": False}


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


def tokenizer(line, tokens):
    array_code = line.split(" ")
    for i in array_code:
        if i == "cmt":
            tokens.append(i)
            break
        tokens.append(i)
    return tokens


def is_equality_exp(s):
    return "=" in s


def get_statement(line, mem_dict, array_code, ln, map_line):
    temp = ln
    line_split = line.split(" ")
    iml_code = return_iml_code("get") + make_two_digit(str(mem_dict[line_split[-1]])) + "00"
    array_code[ln] = iml_code
    ln += 1
    map_line[line_split[0]] = array_code[temp]
    return map_line, array_code, ln


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
        if word == "goto":
            break
        if not word == "let":
            exp += word
    return exp[4:len(exp)]


def get_operator(exp):
    for i in ["=", ">", "<", ]:
        if i in exp:
            return i


def get_register():
    # register = {"01": False, "02": False, "03": False, "04": False}
    for reg, val in register.items():
        if not val:
            register[reg] = True
            return reg
    if register["04"]:
        for reg, val in register.items():
            register[reg] = False
    register["01"] = True
    return list(register.keys())[0]


def let_statement(line, mem_dict, array_code, ln, map_line):
    exp = get_expression(line)
    temp = ln
    if is_expression(exp):
        postfix = p2.infixToPostfix(exp)
        code = p2.postfixEval(postfix, mem_dict)
        code_split = code.split("\n")

        for i in code_split:
            array_code[ln] = i
            ln += 1
    else:
        exp_str = str(exp)
        reg = get_register()
        array_code[ln] = return_iml_code("load") + reg + str(mem_dict[exp_str])
        ln += 1
        array_code[ln] = return_iml_code("store") + reg + str(mem_dict[exp_str])
        ln += 1
    map_line[line.split(" ")[0]] = array_code[temp]
    return map_line, array_code, ln


def if_statement(line, mem_dict, array_code, ln, map_line):
    temp = ln
    line_split = line.split(" ")
    exp = ""
    address = 0
    flag = False

    for s in line_split:
        if not is_reserved(s) and not flag and not line_split.index(s) == 0:
            exp += s
        elif s == "goto":
            flag = True
        elif not is_reserved(s) and flag:
            address = s
    # line_to_go = array_code.index(map_line[address])

    ops = get_operator(exp)
    exp_split_str = exp.split(ops)
    var1 = exp_split_str[0]
    var2 = exp_split_str[1]

    reg1 = get_register()
    reg2 = get_register()

    code = return_iml_code("load") + reg1 + make_two_digit(str(mem_dict[var1])) + "\n"
    code += return_iml_code("load") + reg2 + make_two_digit(str(mem_dict[var2])) + "\n"
    code += return_iml_code("subtract") + reg1 + reg2 + "\n"
    map_line[line_split[0]] = array_code[temp]

    exp = get_expression(line)
    if is_equality_exp(exp):  # use branch zero
        code += return_iml_code("branchzero") + "aa" + make_two_digit(address) + reg1
    else:
        code += return_iml_code("branchpos") + "aa" + make_two_digit(address) + reg1

    for i in code.split("\n"):
        array_code[ln] = i
        ln += 1

    map_line[line_split[0]] = array_code[temp]

    return map_line, array_code, ln


def output_statement(line, mem_dict, array_code, ln, map_line):
    temp = ln
    line_split = line.split(" ")
    iml_code = return_iml_code("output") + make_two_digit(str(mem_dict[line_split[-1]])) + "00"
    array_code[ln] = iml_code
    ln += 1
    map_line[line_split[0]] = array_code[temp]
    return map_line, array_code, ln


def goto_statement(line, mem_dict, array_code, ln, map_line):
    flag = False
    line_split = line.split(" ")
    for token in line_split:
        if token == "goto":
            flag = True
        if flag:
            address = token
    array_code[ln] = "41" + "aa" + make_two_digit(address) + "00"
    map_line[line_split[0]] = array_code[ln]
    ln += 1
    return map_line, array_code, ln


def stop_statement(line, mem_dict, array_code, ln, map_line):
    temp = ln
    array_code[ln] = "990000"
    ln += 1
    map_line[line.split(" ")[0]] = array_code[temp]
    return map_line, array_code, ln
