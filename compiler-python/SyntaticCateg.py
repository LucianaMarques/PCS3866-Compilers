class Token():
    def __init__(self, t, k):
        self.type = t
        self.key = k

class Parser():
    def __init__(self, t):
        self.tokens = t
        for token in self.tokens:
            print(token.key)
    
    def recategorize(self):
        tokens2 = []
        i = 0
        while (i < len(self.tokens)):
            if (self.tokens[i].key == 'FN'):
                tokens2.append(Token('COMPOSED', 'FN' + self.tokens[i+1].key))
                i += 1
            elif (self.tokens[i].key == 'GO'):
                tokens2.append(Token('COMPOSED', 'GOTO'))
                i += 1
            elif (self.tokens[i].key == 'DEF'):
                tokens2.append(Token('COMPOSED','DEFFN'+self.tokens[i+1].key))
                i += 2
            elif (self.tokens[i].key == ">"):
                tokens2.append(Token('COMPOSED', '>='))
                i += 1
            else:
                tokens2.append(self.tokens[i])
            i += 1
        self.tokens = tokens2
