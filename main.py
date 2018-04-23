import sys
import p2336 as p2

def is_operator(s):
    return s in ["+", "-", "/", "*", "^", "%", "=", ">", "<", "!=", "(", ")"]


# check to see a given string, s, is a reserved word
def is_reserved(s):
    return s in ["get", "output", "goto", "stop", "let", "if"]


def tokenizer(fileName):
    """
        :parameter f: the file passed from the main program
        :type f: file
        :return tokens: array
    """
    with open(fileName, "r") as f:
        tokens = []
        for frl in f.readlines():
            frll = frl.replace("\n", "").split(" ")
            for i in frll:
                if i == "cmt":
                    tokens.append(i)
                    break
                tokens.append(i)
    return tokens


def make_symbol_table(fileName):
    min_mem = 0
    max_mem = 99

    table = []
    dup = []
    with open(fileName, "r") as f:
        for frl in f.readlines():
            frll = frl.replace("\n", "").split(" ")
            for i in frll:
                if i not in dup:
                    if i == "goto" or i == "cmt":
                        break
                    if frll.index(i) == 0:
                        table.append(["L", frll[0], min_mem])
                        min_mem += 1
                    elif not (is_operator(i)) and not (is_reserved(i)):
                        if i.isdigit():
                            table.append(["C", i, max_mem])
                            max_mem -= 1
                        elif i.isalpha() or i.isalnum():
                            table.append(["V", i, max_mem])
                            max_mem -= 1
                        dup.append(i)
    return table



def main():
    
    file_path = "./plain/text.txt"
    table = make_symbol_table(file_path)
    for i in table:
        print(i)






    tokens = tokenizer(file_path)
    print(tokens)



if __name__ == '__main__':
    main()
