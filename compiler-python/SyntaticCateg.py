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
            if (self.tokens[i].key == 'FN'):
                #print('FN')
                tokens2.append(Token('COMPOSED', 'FN' + self.tokens[i+1].key))
                i += 1
            elif (self.tokens[i].key == 'GO'):
                #print('GO')
                tokens2.append(Token('COMPOSED', 'GOTO'))
                i += 1
            elif (self.tokens[i].key == 'DEF'):
                #print('DEF')
                tokens2.append(Token('COMPOSED','DEF FN '+self.tokens[i+2].key))
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
                pass
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
                while(self.tokens[j]!=EOL):
                    j += 1
                proximo = j - i
            
            elif(self.check_end(i)):
                self.codeGenerator.print_module()
        
        # add a new variable to the global variables' table
        elif(self.automaton_state.id == 3):
            # self.variables.append((self.tokens[i].key,self.tokens[i+2].key))
            # print(self.tokens[i].key,self.tokens[i+2].key)
            self.codeGenerator.generate_global_variable(self.tokens[i].key,int(self.tokens[i+2].key))
            proximo = 3
        
        # print an identifier's value
        elif(self.automaton_state.id == 8):
            pass

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