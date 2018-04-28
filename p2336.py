# Phat Phan, Kevin Sie, Daniel Rodriguez
# La Salle University, CSC366, Spring 2018
# Project 2: Infix to Postfix
# Download link: https://www.python.org/downloads/
# The project is written on Python 3 version

import sys

# re - regex class: helps to deal with variables that contain 2 or more letter for example a1, a2, 9562 or omg.
import re

import util


# Daniel provided two build-in methods of Python that can handle better than regex. They are isalnum() and isdigit().
# However, in the loop to ask users if they want to do another expression, it's simpler with regex.

# The advantage of Python 3 is that when it breaks the string input into tokens,
# each token will automatically be separated by blank space.
# For example A1 + 6 will give A1 6 +

# The disadvantage is when users input without any space, there will be an error.
# For example, a+5, a+ 5 because when it splits the input, it will see a+5 or a+ as a whole token
# Kevin provided fix_space method to handle tokens with or without space

# Define a class (stack) - that has 5 methods. We will use push and pop and peek to work on each token
# The other 4 are used for checking
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    # Go back 1 position in the stack
    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def is_expression(string):
    return string in ["+", "-", "/", "*"]


# Method to convert infix to postfix
def infixToPostfix(userInput):
    prec = {}
    prec["^"] = 3
    prec["%"] = 2
    prec["*"] = 2
    prec["/"] = 2
    prec["+"] = 1
    prec["-"] = 1
    prec["("] = 0

    # Create a stack to hold the left parenthesis and all operations +-*/%^ and variables
    operation = Stack()

    # Create the array that holds postfix output
    postfixList = []

    # Array to hold breaking down input as tokens
    tokenList = fix_spaces(userInput).split()

    # Loop through each token
    # Check if each token is a variable, number, letter, or left-right parenthesis
    # When it sees a  right parenthesis meaning the end of an expression
    # (it may a small expression inside a bigger expression)
    # It will pop everything in the operation stack to the postfixList

    for token in tokenList:
        # If re.search('[a-zA-Z]', token) or token in str(list(range(10000))): old manually check
        if token.isalnum():
            postfixList.append(token)
        elif token == '(':
            operation.push(token)
        elif token == ')':
            topToken = operation.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = operation.pop()
        else:
            while (not operation.isEmpty()) and (prec[operation.peek()] >= prec[token]):
                postfixList.append(operation.pop())
            operation.push(token)
    # Pop out everything in the operation stack to the postfixList
    while not operation.isEmpty():
        postfixList.append(operation.pop())
    return " ".join(postfixList)


# Postfix evaluation method, if the expressions contain only number
# It will calculate output
def postfixEval(postfixExpr, mem_dict):
    # Create stack to hold all arithmetic operations and number
    operandStack = Stack()
    # postfixExpr is the result of inFixtoPostfix method
    tokenList = postfixExpr.split()
    stack = []
    mem = []
    code = ""
    # Loop through the list
    # It checks 3 tokens from left to right at a time

    # For example 6 3 + 6 - meaning 6 + 3 = 9 then 9 - 6 = 3
    for token in tokenList:
        # If token in str(list(range(19998))): old manually check
        if token.isdigit() or token.isalpha():
            reg = util.get_register()
            stack.append(reg)
            mem.append(mem_dict[token])
            code += util.return_iml_code("load") + reg + util.make_two_digit(str(mem_dict[token])) + "\n"
            # operandStack.push(int(token))
        else:
            # operand2 = operandStack.pop()
            # operand1 = operandStack.pop()
            # result = doMath(token, operand1, operand2)
            # operandStack.push(result)
            reg2 = stack.pop()
            mem2 = mem.pop()
            reg1 = stack.pop()
            mem1 = mem.pop()

            code += util.return_iml_code(util.ops_to_string(token)) + reg1 + reg2 + "\n"
            code += util.return_iml_code("store") + reg1 + str(mem1)

            # while not stack:
            #     code += stack.pop()
            #     print(code)
    # print(stack)
    # return operandStack.pop()
    return code

# Method to calculate the postfix
def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    elif op == "%":
        return op1 % op2
    elif op == "^":
        return op1 ** op2
    else:
        return op1 - op2


# Kevin gave a great method: strip spaces out and replace them with ones we want
def fix_spaces(string):
    precedence = ["^", "%", "*", "/", "+", "-", "(", ")"]

    temp = string.replace(" ", "")

    for tok in temp:
        if tok in precedence:
            temp = temp.replace(tok, " " + tok + " ")
    return temp


# This is the main method that will call other method
def main():
    # A loop to ask user if they want to continue or not
    while True:
        # Read user input
        expression = input('Please enter your expression!\n')

        # Check if input contains just characters, number, or both
        # If input contain just characters or both characters and number,
        # then use infixtoposstfix method without evaluation
        # If the input contain only numbers then evaluate it.

        c = True
        check = expression.split()
        for char in check:
            if re.search('[a-zA-Z]', char):
                c = False

        if c:
            print("This is the Postfix:")
            print(infixToPostfix(expression))
            print("This is the evaluation result:")
            print(postfixEval(infixToPostfix(expression)))
        else:
            print("This is the Postfix:")
            print(infixToPostfix(expression))

        # Ask user if they want to continue
        again = input("\nDo you want to continue?  Y/N\n").lower()
        if again == "y":
            continue
        else:
            break
    sys.exit()


if __name__ == '__main__':
    main()
