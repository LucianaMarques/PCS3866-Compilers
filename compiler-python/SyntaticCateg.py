import math
from CodeGenerator import CodeGenerator

# Dictionaries used
functions = {}
functions_stack = []
variables_symbols = {}
current_variable = []

class SintaxAutomaton():
    def __init__(self):
        self.id = 1

class Token():
    def __init__ (self, t, k):
        self.type = t
        self.key = k

class Syntax():
    def __init__ (self, t):
        self.tokens = t
        self.name = None

class Parser():
    def __init__(self):
        self.tokens = []
        self.sintaxes = []
        self.automaton_state = SintaxAutomaton()
        self.codeGenerator = CodeGenerator()

        # current token none by default
        self.current_token = None
        self.current_token_id = 0

        # current variable being assigned
        self.current_variable = ""

        # global variable table
        self.variables = {}

        # global function table
        self.functions = {}

        # variables in FOR loops
        self.for_variables = {}
        self.last_for_loops = []
    
    def initialize_tokens(self):
        self.current_token = self.tokens[0]

    def extract_token(self):
        self.current_token = self.tokens[self.current_token_id]
        self.current_token_id += 1

    def recategorize_tokens(self):
        tokens2 = []
        i = 0
        while (i < len(self.tokens)):
            if (self.tokens[i].key == 'GO'):
                #print('GO')
                tokens2.append(Token('COMPOSED', 'GOTO'))
                i += 1
            elif (self.tokens[i].key == 'DEF'):
                tokens2.append(Token('COMPOSED','DEF FN '))
                tokens2.append(Token(self.tokens[i+2].type, self.tokens[i+2].key))
                i += 2
            elif (self.tokens[i].key == ">"):
                tokens2.append(Token('COMPOSED', '>='))
                i += 1
            else:
                tokens2.append(self.tokens[i])
            i += 1
        self.tokens = tokens2

    def syntax_categorize(self):
        i = 0 
        while (i < len(self.tokens)):
            print("TOKEN: ", self.tokens[i].type, self.tokens[i].key, "ESTADO: ", self.automaton_state.id)
            proximo = self.next_state(i)
            i += proximo
    
    def syntax_extraction(self):
        self.initialize_tokens()
        while (self.current_token_id < len(self.tokens)):
            print("ESTADO: ", self.automaton_state.id, " TOKEN:", self.current_token.type, self.current_token.key)
            self.next_state()
            self.extract_token()

    def next_state(self):
        if (self.current_token.type == "EOL"):
            self.automaton_state.id = 1

        elif(self.current_token.type == "INT"):
            if (self.automaton_state.id == 1):
                self.automaton_state.id = 2
            elif (self.automaton_state.id == 6):
                # print("hey")
                # look for in the variable tables for the correspondent value
                # print(self.currant_variable)
                variables_symbols[self.currant_variable] = int(self.current_token.key)
                #print(variables_symbols[self.currant_variable])
                # skip state 7
                # self.automaton_state.id = 8
                # variables_symbols[self.current_variable] = int(self.current_token.key)
                # self.extract_token()print
            elif(self.automaton_state.id == 54 or self.automaton_state.id == 53):
                self.automaton_state.id = 55
        
        elif(self.current_token.type == "RESERVED"):
            if (self.current_token.key == "LET"):
                self.automaton_state.id = 4
            elif (self.current_token.key == "PRINT"):
                self.automaton_state.id = 11
            elif (self.current_token.key == "DATA"):
                self.automaton_state.id = 21
            elif (self.current_token.key == "GOTO"):
                self.automaton_state.id = 23
            elif (self.current_token.key == "GO"):
                self.automaton_state.id = 23
                self.extract_token() # skip "TO"
            elif (self.current_token.key == "IF"):
                self.automaton_state.id = 25
            elif (self.current_token.key == "FOR"):
                print("BEGINING OF A FOR LOOP")
                self.extract_token()
                self.currant_variable = self.current_token.key
                self.extract_token()
                self.extract_token()
                current_state = int(self.current_token.key)
                self.extract_token()
                self.extract_token()
                final_state = int(self.current_token.key)
                self.for_variables[self.currant_variable] = (current_state,final_state,self.current_token_id)
                self.variables[self.currant_variable] = current_state
                self.last_for_loops.append(self.currant_variable)
                # self.automaton_state.id = 32
                self.automaton_state.id = 1
                print("CURRENT STATE: ",self.currant_variable, " = ", current_state)
                print("FINAL STATE  : ",self.currant_variable, " = ", final_state)
            elif (self.current_token.key == "NEXT"):
                print("END OF FOR BLOCK, EVALUATING IF REPETITION IS NEEDED")
                self.extract_token()
                (init,final,destination_id) = self.for_variables[self.current_token.key]
                init = init + 1
                print("CURRENT STATE: ",self.current_token.key, " = ", init)
                print("FINAL STATE  : ",self.current_token.key, " = ", final)
                if (init > final):
                    self.extract_token()
                    self.automaton_state.id = 1
                else:
                    self.current_token_id = destination_id
                    self.for_variables[self.current_token.key] = (init,final,destination_id)
                self.variables[self.current_token.key] = init
                # self.automaton_state.id = 41
            elif (self.current_token.key == "DIM"):
                self.automaton_state.id = 43
            elif (self.current_token.key == "GOSUB"):
                self.automaton_state.id = 58
            elif (self.current_token.key == "REM"):
                while(self.current_token.type != "EOL"):
                    self.extract_token()
                self.automaton_state.id = 18
            elif (self.current_token.key == "END"):
                self.automaton_state.id = 3
            elif (self.current_token.key == "READ"):
                self.extract_token()
                print("READING VARIABLE")
                self.currant_variable = self.current_token.key
                value = int(input("Type the value: "))
                variables_symbols[self.currant_variable] = value
                print(variables_symbols[self.currant_variable])
                self.automaton_state.id = 1
            elif (self.current_token.key == "FN" or self.current_token.key == "FN "):
                self.automaton_state.id = 56
            
            # PREDEF
            elif (self.automaton_state.id == 53 or self.automaton_state.id == 54):
                self.automaton_state.id = 57

        elif(self.current_token.type == "COMPOSED"):
            # register new function
            if(self.current_token.key == "DEF FN "):
                self.automaton_state.id = 48
        
        elif(self.current_token.type == "CHARACTER"):
            if (self.automaton_state.id == 4):
                # print(self.current_token.type)
                self.currant_variable = self.current_token.key
                self.automaton_state.id = 5
            elif (self.automaton_state.id == 5):
                self.automaton_state.id = 6
                self.extract_token()
                print(self.current_token.type)
                expression = []
                print("EXTRACTING EXPRESSION")
                while(self.current_token.type != 'EOL'):
                    # print(self.current_token.type)
                    expression.append(self.current_token)
                    self.extract_token()
                result = self.calculate_expression(expression)
                variables_symbols[self.currant_variable] = result
                #print(variables_symbols[self.currant_variable])
                self.automaton_state.id = 1
            elif (self.automaton_state.id == 11):
                print("COMPILER ACTION")
                if (self.current_token.key in variables_symbols):
                    print(variables_symbols[self.current_token.key])
                else:
                    print(self.current_token.key)
            elif (self.automaton_state.id == 48):
                # function name
                self.currant_variable = self.current_token.key
                self.automaton_state.id = 49
            elif (self.automaton_state.id == 49):
                self.automaton_state.id = 50
            elif (self.automaton_state.id == 50):
                functions[self.currant_variable] = (self.current_token.key,[])
                self.automaton_state.id = 51
            elif (self.automaton_state.id == 51):
                self.automaton_state.id = 52
            elif (self.automaton_state.id == 52):
                # print(self.currant_variable)
                # self.automaton_state.id = 53
                variable, expression = functions[self.currant_variable]
                # print(variable)
                while(self.current_token.type != 'EOL'):
                    # print(self.current_token.type)
                    expression.append(self.current_token)
                    self.extract_token()
                functions[self.currant_variable] = (variable,expression)
                print("FUNCTION ", self.currant_variable, " DEFINED")
                self.automaton_state.id = 1
            elif (self.automaton_state.id == 53):
                # variable, expression = functions[self.currant_variable]
                # while(self.current_token.type != 'EOL'):
                #     expression.append(self.current_token)
                #     self.next_state()
                #     self.extract_token()
                # functions[self.currant_variable] = (variable,expression)
                # self.automaton_state.id = 1
                if (self.current_token.key == '+' or self.current_token.key == '-'):
                    self.automaton_state.id = 54
                else:
                    self.automaton_state.id = 55
            elif (self.automaton_state.id == 54):
                self.automaton_state.id = 53
            elif (self.automaton_state.id == 55):
                if (self.current_token.key == ")"):
                    self.automaton_state.id = 58
                else:
                    # + - * / ^
                    self.automaton_state.id = 54
            elif (self.automaton_state.id == 56):
                self.automaton_state.id = 57
            elif (self.automaton_state.id == 57):
                self.automaton_state.id = 53
            elif (self.automaton_state.id == 58):
                self.automaton_state.id = 55

        elif(self.current_token.type == "NUM"):
            if (self.automaton_state.id == 6):
                self.automaton_state.id = 8
            elif (self.automaton_state.id == 7):
                if (self.currant_variable is not None):
                    variables_symbols[self.currant_variable] = self.current_token.key
                    current_variable = None
                    self.automaton_state.id = 8
            elif (self.automaton_state.id == 54):
                self.automaton_state.id = 55

        elif(self.current_token.type == "SNUM"):
            if (self.automaton_state.id == 6):# Cria a regra
                pass
    
    def calculate_function_expression(self,variable_name,variable_value,tokens):
        print("EVALUATING FUNCTION EXPRESSION")
        print("VARIABLE VALUE ",variable_value)
        # print(len(tokens))
        exp_stack = []
        result = 0
        i = 0
        while (i < len(tokens)):
            # print("i: ", i)
            # print(tokens[i].key)
            if (tokens[i].key == variable_name):
                if (len(exp_stack) == 0):
                    result += variable_value
                else:
                    result = self.calculate_operation(exp_stack.pop(),result,variable_value)
            elif (tokens[i].type == 'INT'):
                if (len(exp_stack) == 0):
                    result += int(tokens[i].key)
                else:
                    result = self.calculate_operation(exp_stack.pop(),result,int(tokens[i].key))
            elif (tokens[i].type == 'CHARACTER'):
                if (tokens[i].key == '('):
                    print("FOUND NEW EXPRESSION")
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        if (tokens[i].key == variable_name):
                            print("CHANGE TOKEN KEY TO ", variable_value)
                            token = Token('INT',variable_value)
                            expression.append(token)
                        else:
                            expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = self.calculate_expression(expression)
                    print("Partial result: ", partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                    else:
                        result = self.calculate_operation(exp_stack.pop(),result,partial_result)
                elif (tokens[i].key == ')'):
                    return result
                elif (tokens[i].key == '*' or tokens[i].key == '^' or tokens[i].key == '+' or tokens[i].key == '/' or tokens[i].key == '-'):
                    exp_stack.append(tokens[i].key)
                    print("appended character expression")
            i = i + 1
        print("Result: ",result)
        print("END OF FUNCTION EVALUATION")
        return result

    def calculate_expression(self,tokens):
        exp_stack = []
        result = 0
        i = 0
        # print(len(tokens))
        while (i < len(tokens)):
            print("CURRENT EXPRESSION TOKEN: ",tokens[i].key)
            if (tokens[i].type == 'CHARACTER'):
                if (tokens[i].key == '('):
                    print("FOUND NEW EXPRESSION")
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = self.calculate_expression(expression)
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                    else:
                        result = self.calculate_operation(exp_stack.pop(),result,partial_result)
                elif (tokens[i].key == ')'):
                    return result
                elif (tokens[i].key == '*' or tokens[i].key == '^' or tokens[i].key == '+' or tokens[i].key == '/' or tokens[i].key == '-'):
                    exp_stack.append(tokens[i].key)
                    print("appended character expression")
            elif (tokens[i].type == 'INT'):
                if (len(exp_stack) == 0):
                    # print("added to the result")
                    result = int(tokens[i].key)
                else:
                    exp = exp_stack.pop()
                    result = self.calculate_operation(exp,result,int(tokens[i].key))
            elif (tokens[i].type == 'RESERVED'):
                if (tokens[i].key == 'EXP'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ")"):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.exp(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'SQR'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.sqrt(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'SIN'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.sin(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'COS'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.cos(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'TAN'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.tan(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'ABS'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = abs(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'LOG'):
                    expression = []
                    i += 1
                    while (tokens[i].key != ')'):
                        expression.append(tokens[i])
                        i += 1
                    expression.append(tokens[i])
                    i += 1
                    partial_result = math.log(self.calculate_expression(expression))
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
                elif (tokens[i].key == 'FN'):
                    i += 1
                    function_name = tokens[i].key
                    print("FUNCTION NAME ", function_name)
                    variable,expression = functions[function_name]
                    print("FUNCTION VARIABLE ",variable)
                    i += 2
                    variable_value = 0
                    if (tokens[i].type == 'INT'):
                        variable_value = int(tokens[i].key)
                    else:
                        variable_value = self.variables[variable]
                        print("FOUND VARIABLE ",variable, " ",variable_value)
                    partial_result = self.calculate_function_expression(variable,variable_value,expression)
                    # print(partial_result)
                    if (len(exp_stack) == 0):
                        result = partial_result
            i += 1
        print("END OF EXPRESSION CALCULATION")
        return result

    def calculate_operation(self,exp,result,partial_result):
        if (exp == '^'):
            result = result**partial_result
        elif (exp == '/'):
            result = result/partial_result
        elif (exp == '*'):
            result = result*partial_result
        elif (exp == '+'):
            result = result+partial_result
        elif (exp == '-'):
            result = result-partial_result
        return result

    