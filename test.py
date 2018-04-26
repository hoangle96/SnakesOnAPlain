def is_operator(s):
    return s in ["+", "-", "/", "*", "^", "%", ">", "<", "!=", "(", ")"]


def check_expression(string):
    for i in string:
        if is_operator(i):
            return True
    return False

def main():
    print(check_expression("x + 3"))

if __name__ == '__main__':
    main()