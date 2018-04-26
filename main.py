import sys
import p2336 as p2

import util


# def tokenizer(fileName):
#     """
#         :parameter f: the file passed from the main program
#         :type f: file
#         :return tokens: array
#     """
#     with open(fileName, "r") as f:
#         tokens = []
#         for frl in f.readlines():
#             frll = frl.replace("\n", "").split(" ")
#             for i in frll:
#                 if i == "cmt":
#                     tokens.append(i)
#                     break
#                 tokens.append(i)
#     return tokens


# def make_symbol_table(fileName):
#     min_mem = 0
#     max_mem = 99
#
#     table = []
#     dup = []
#     with open(fileName, "r") as f:
#         for frl in f.readlines():
#             frll = frl.replace("\n", "").split(" ")
#             for i in frll:
#                 if i not in dup:
#                     if i == "goto" or i == "cmt":
#                         break
#                     if frll.index(i) == 0:
#                         table.append(["L", frll[0], min_mem])
#                         min_mem += 1
#                     elif not (util.is_operator(i)) and not (util.is_reserved(i)):
#                         if i.isdigit():
#                             table.append(["C", i, max_mem])
#                             max_mem -= 1
#                         elif i.isalpha() or i.isalnum():
#                             table.append(["V", i, max_mem])
#                             max_mem -= 1
#                         dup.append(i)
#     return table


# def make_symbol_table(fileName, array_code):
#     min_mem = 0
#     max_mem = 99
#
#     table = []
#     dup = []
#
#     dict = {}
#
#     flag = False
#     with open(fileName, "r") as f:
#         for frl in f.readlines():
#             frll = frl.replace("\n", "").split(" ")
#             for i in frll:
#                 if "goto" in frll:
#                     flag = True
#                 else:
#                     flag = False
#                 if i not in dup:
#                     if i == "goto" or i == "cmt":
#                         break
#                     if frll.index(i) == 0:
#                         if flag:
#                             table.append(["L", frll[0], min_mem, "yes"])
#                         else:
#                             table.append(["L", frll[0], min_mem, "no"])
#                         min_mem += 1
#                     elif not (util.is_operator(i)) and not (util.is_reserved(i)):
#                         if i.isdigit():
#                             table.append(["C", i, max_mem])
#                             dict[i] = max_mem
#                             max_mem -= 1
#                         elif i.isalpha() or i.isalnum():
#                             table.append(["V", i, max_mem])
#                             dict[i] = max_mem
#                             max_mem -= 1
#                         dup.append(i)
#     return table, dict, array_code


def print_file(file_name, array_code):
    """
    :parameter file_name: the name of the output file
    :type file_name: string
    :parameter array_code: the IML code
    :type array_code: array
    :return f: file
    """
    # delete any previous code in the file
    with open(file_name, "w") as f:
        f.write("")

    # output the code
    with open(file_name, "a+") as f:
        for i in array_code:
            f.write(i + "\n")
        return f


def main():
    max_mem = 99
    min_mem = 00
    ln = 0
    array_code = ["000000"] * 100

    file_path = "./plain/text.txt"
    file_name = "./output/iml.txt"

    with open(file_path, "r+") as f:
        content = f.read()
        tokens = util.tokenizer(content)
        sym_table, mem_dict = util.make_symbol_table(content)
        content_by_line = content.split("\n")
        for line in content_by_line:
            if "get" in line:
                array_code, ln = util.get_statement(line, mem_dict, array_code, ln)
            elif "let" in line:
                array_code, ln = util.let_statement(line, mem_dict, array_code, ln)


    array_code[ln] = "990000"
    print(array_code)
    # print(array_code)
    # print_file(file_name, array_code)


if __name__ == '__main__':
    main()
