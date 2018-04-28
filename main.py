import sys
import p2336 as p2

import util


def print_file(file_name, array_code):
    """
    :parameter file_name: the name of the output file
    :type file_name: string
    :parameter array_code: the IML code
    :type array_code: array
    :return f: file
    """
    # delete any previous code in the file
    with open(file_name, "w+") as f:
        f.write("")

    # output the code
    with open(file_name, "a+") as f:
        for i in array_code:
            f.write(i + "\n")
        return f


dup = []


def make_symbol_table(line, table, mem_dict, min_mem, max_mem, array_code):
    flag = False

    if "goto" in line:
        flag = True

    line_split = line.split(" ")
    for i in line_split:
        if i not in dup:
            if i == "cmt" or i == "goto":
                break
            if line_split.index(i) == 0:
                table.append(["L", line_split[0], min_mem, flag])
                min_mem += 1
            elif not (util.is_operator(i)) and not (util.is_reserved(i)):
                if i.isdigit():
                    table.append(["C", i, max_mem])
                    mem_dict[i] = max_mem
                    array_code[max_mem] = util.make_two_digit(i)
                    max_mem -= 1
                elif i.isalpha() or i.isalnum():
                    table.append(["V", i, max_mem])
                    mem_dict[i] = max_mem
                    max_mem -= 1
                dup.append(i)
    return table, mem_dict, min_mem, max_mem, array_code


def main():
    array_code = ["000000"] * 100
    ln = 0
    file_path = "./plain/text.txt"
    file_name = "./output.txt"

    min_mem = 0
    max_mem = 99

    mem_dict = {}
    tokens = []
    sym_table = []

    map_line = {}

    with open(file_path, "r+") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            tokens = util.tokenizer(line, tokens)
            sym_table, mem_dict, min_mem, max_mem, array_code = make_symbol_table(line, sym_table, mem_dict, min_mem, max_mem, array_code)
            if "get" in line:
                map_line, array_code, ln = util.get_statement(line, mem_dict, array_code, ln, map_line)
            elif "let" in line:
                map_line, array_code, ln = util.let_statement(line, mem_dict, array_code, ln, map_line)
            elif "if" in line:
                map_line, array_code, ln = util.if_statement(line, mem_dict, array_code, ln, map_line)
            elif "goto" in line:
                map_line, array_code, ln = util.goto_statement(line, mem_dict, array_code, ln, map_line)
            elif "output" in line:
                map_line, array_code, ln = util.output_statement(line, mem_dict, array_code, ln, map_line)
            elif "stop" in line:
                map_line, array_code, ln = util.stop_statement(line, mem_dict, array_code, ln, map_line)

    for iml in array_code:
        if len(iml) > 6:
            if iml[0:2] == util.return_iml_code("branch"):
                index = array_code.index(iml)
                address = iml[4:6]
                iml = util.return_iml_code("branch") + util.make_two_digit(str(array_code.index(map_line[address]))) +"00"
                array_code[index] = iml
            else:
                index = array_code.index(iml)
                op_code = iml[0:2]
                reg = iml[-2:]
                address = iml[4:6]
                iml = op_code + util.make_two_digit(str(array_code.index(map_line[address]))) + reg
                array_code[index] = iml

    for entry in sym_table:
        if entry[0] == "C":
            array_code[entry[2]] = "0000" + util.make_two_digit(entry[1])

    # print(tokens)
    # print(sym_table)
    # print(array_code)
    # print(mem_dict)
    # print(map_line)

    print(mem_dict)

    for i in array_code:
        print(i)



    # array_code[ln] = "990000"
    # print(array_code)

    print_file(file_name, array_code)
    # print("The file is called 'output.txt', at the same folder of the main file.")
    # print(sym_table)


if __name__ == '__main__':
    main()
