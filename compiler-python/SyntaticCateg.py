class SintaxAutomaton():
    def __init__(self):
        self.id = 1

class Token():
    def __init__ (self, t, k):
        self.type = t
        self.key = k

class Syntax()
    def __init__ (self, t):
        self.tokens = t
        self.name = None

class Parser():
    def __init__(self):
        self.tokens = []
        self.sintaxes = []
        self.automaton_state = SintaxAutomaton()
    
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
        for token in self.tokens:
            pass
    
    def next_state(self, i):
        
