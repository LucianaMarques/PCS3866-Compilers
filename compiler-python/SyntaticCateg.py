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
            print(i)
    
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
                print("hey")
                # look for in the variable tables for the correspondent value
                print(self.currant_variable)
                variables_symbols[self.currant_variable] = int(self.current_token.key)
                print(variables_symbols[self.currant_variable])
                # skip state 7
                # self.automaton_state.id = 8
                # variables_symbols[self.current_variable] = int(self.current_token.key)
                # self.extract_token()
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
                self.automaton_state.id = 32
            elif (self.current_token.key == "NEXT"):
                self.automaton_state.id = 41
            elif (self.current_token.key == "DIM"):
                self.automaton_state.id = 43
            elif (self.current_token.key == "GOSUB"):
                self.automaton_state.id = 58
            elif (self.current_token.key == "REM"):
                self.automaton_state.id = 18
            elif (self.current_token.key == "END"):
                self.automaton_state.id = 3
            elif (self.current_token.key == "READ"):
                self.automaton_state.id = 19
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
                self.currant_variable = self.current_token.key
                self.automaton_state.id = 5
            elif (self.automaton_state.id == 5):
                self.automaton_state.id = 6
            elif (self.automaton_state.id == 11):
                print("COMPILER ACTION")
                if (self.current_token.key in variables_symbols):
                    print(variables_symbols[self.current_token.key])
                else:
                    print(self.current_token.key)
            elif (self.automaton_state.id == 48):
                self.automaton_state.id = 49
            elif (self.automaton_state.id == 49):
                # Add the function's name to the function dictionary
                functions[self.current_token.key] = ()
                functions_stack.append(self.current_token.key)
                self.automaton_state.id = 50
            elif (self.automaton_state.id == 50):
                functions_stack.append(self.current_token.key)
                self.automaton_state.id = 51
            elif (self.automaton_state.id == 51):
                if self.automaton_state.id == 'INT':
                    functions_stack.append(self.current_token.key)
                    self.automaton_state.id = 51
                else:
                    # finish populating the functions map
                    variable = ""
                    i = 1
                    while (i < len(functions_stack)):
                        variable = variable + functions_stack[i]
                    functions[functions_stack[0]] = (variable)
                    self.automaton_state.id = 52
            elif (self.automaton_state.id == 52):
                self.automaton_state.id = 53
            elif (self.automaton_state.id == 53):
                variable = functions[functions_stack[0]][0]
                if (self.current_token.key == "+" or self.current_token.key == "-"):
                    functions[functions_stack[0]] = (variable,60)
                    self.automaton_state.id = 54
                else:
                    functions[functions_stack[0]] = (variable,61)
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
    