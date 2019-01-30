from CodeGenerator import CodeGenerator

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

        # global variable table
        self.variables = []
    
    def recategorize_tokens(self):
        tokens2 = []
        i = 0
        while (i < len(self.tokens)):
            # if (self.tokens[i].key == 'FN'):
            #     #print('FN')
            #     tokens2.append(Token('COMPOSED', 'FN' + self.tokens[i+1].key))
            #     i += 1
            # elif (self.tokens[i].key == 'GO'):
            if (self.tokens[i].key == 'GO'):
                #print('GO')
                tokens2.append(Token('COMPOSED', 'GOTO'))
                i += 1
            elif (self.tokens[i].key == 'DEF'):
                #print('DEF')
                tokens2.append(Token('COMPOSED','DEF FN '))
                tokens2.append(Token(self.tokens[i+2].type, self.tokens[i+2].key))
                i += 2
            elif (self.tokens[i].key == ">"):
                #print('>')
                tokens2.append(Token('COMPOSED', '>='))
                i += 1
            else:
                tokens2.append(self.tokens[i])
            i += 1
        self.tokens = tokens2

    def syntax_categorize(self):
        i = 0
        while (i < len(self.tokens)):
            print("TOKEN: ", self.tokens[i].type, self.tokens[i].key)
            proximo = self.next_state(i)
            i += proximo
    
    def next_state(self, i):
        proximo = 1

        if (self.tokens[i].type == "EOL"):
            self.automaton_state.id = 1

        elif (self.automaton_state.id == 1):
            self.automaton_state.id = 2

        elif (self.automaton_state.id == 2):
            # create a new variable and assign it its value
            if (self.check_assign(i)):
                self.automaton_state.id = 3

            elif(self.check_data(i)):
                pass
            elif(self.check_def(i)):
                self.automaton_state.id = 12
                
            elif(self.check_dim(i)):
                pass
            elif(self.check_for(i)):
                pass
            elif(self.check_gosub(i)):
                pass
            elif(self.check_goto(i)):
                pass
            elif(self.check_if(i)):
                pass
            elif(self.check_next(i)):
                pass
            elif(self.check_print(i)):
                self.automaton_state.id = 8

            elif(self.check_read(i)):
                pass
            
            # Do not make anything when REM
            elif(self.check_rem(i)):
                j = i
                while(self.tokens[j].type!='EOL'):
                    j += 1
                proximo = j - i
            
            elif(self.check_end(i)):
                self.codeGenerator.generate_code()
        
        # add a new variable to the global variables' table
        elif(self.automaton_state.id == 3):
            # self.variables.append((self.tokens[i].key,self.tokens[i+2].key))
            # print(self.tokens[i].key,self.tokens[i+2].key)
            value = self.get_expression_value()
            self.codeGenerator.generate_global_variable(self.tokens[i].key,value)
            proximo = 3
        
        # print an identifier's value
        elif(self.automaton_state.id == 8):
            self.codeGenerator.printf_id(self.tokens[i].key)

        elif(self.automaton_state.id == 12):
            # ex: DEF FN N(X)
            name = self.tokens[i].key[0]
            variable = self.tokens[i].key[2]
            # assume-se tipo da função sempre DOUBLE
            self.codeGenerator.generate_user_function(name,variable)

        return proximo

    def check_assign(self,i):
        if (self.tokens[i].key != 'LET'):
            return False
        else:
            return True
    
    def check_read(self,i):
        if (self.tokens[i].key != 'READ'):
            return False
        else:
            return True
    
    def check_data(self,i):
        if (self.tokens[i].key != 'DATA'):
            return False
        else:
            return True
    
    def check_print(self,i):
        if (self.tokens[i].key != 'PRINT'):
            return False
        else:
            return True
    
    def check_goto(self,i):
        if (self.tokens[i].key != 'GOTO' or self.tokens[i].key != 'GO'):
            return False
        else:
            return True

    def check_if(self,i):
        if (self.tokens[i].key != 'IF'):
            return False
        else:
            return True
    
    def check_for(self,i):
        if (self.tokens[i].key != 'FOR'):
            return False
        else:
            return True
    
    def check_next(self,i):
        if (self.tokens[i].key != 'NEXT'):
            return False
        else:
            return True

    def check_dim(self,i):
        if (self.tokens[i].key != 'DIM'):
            return False
        else:
            return True
    
    def check_def(self,i):
        if (self.tokens[i].key != 'DEF FN'):
            return False
        else:
            return True
    
    def check_gosub(self,i):
        if (self.tokens[i].key != 'GOSUB'):
            return False
        else:
            return True

    # Does not generate code! Only for remark purposes
    def check_rem(self,i):
        if (self.tokens[i].key != 'REM'):
            return False
        else:
            return True
    
    def check_end(self, i):
        if (self.tokens[i].key != 'END'):
            return False
        else:
            return True

    def get_expression_value(self, i):
        proximo = i
        negative = 0
        operation = 0
        # verifica se é negativo
        if (tokens[i].key == '-'):
                negative = 1
                proximo += 1
        value = 0
        while(tokens[proximo].type != EOL):
            if (tokens[proximo].key == '+'):
                operation = 1
            elif(tokens[proximo].key == '-'):
                operation = 2
            elif (tokens[proximo].key == '*'):
                operation = 3
            elif(tokens[proximo].key == '/'):
                operation = 4
            else:
                eb = self.check_eb()
                if (operation == 0):
                    value = eb
                    if negative:
                        value = -value
                elif (operation == 1):
                    value += eb
                elif (operation == 2):
                    value -= eb
                elif (operation == 3):
                    value = eb*value
                elif (operation == 4):
                    value = value/eb
            proximo += 1
        return value

    def check_eb(self, i):
        # verifica se é número
        if(self.tokens[i].type == INT):
            return int(self.tokens[i].char)
        # varifica se é variável global
        elif(self.tokens[i].type == CHARACTER):
            if (self.tokens[i].key in self.variables):
                return int(self.variables[tokens[i].key])
            elif (self.tokens[i].char == "FN"):
                return self.calculate_function(i)
        elif(tokens[i].type == RESERVED):
            # manda uma flag para o codeGenerator
            if (tokens[i].key == "SIN"):
                pass
            elif (tokens[i].key == "COS"):
                pass
            elif (tokens[i].key == "TAN"):
                pass
            elif (tokens[i].key == "EXP"):
                pass
            elif (tokens[i].key == "ABS"):
                pass
            elif (tokens[i].key == "LOG"):
                pass
            elif (tokens[i].key == "SQR"):
                pass
        return 0