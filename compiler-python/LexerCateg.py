from SyntaticCateg import Token

# global variables for automaton states
IDENTIFIER = 3
CHARACTER = 4
INT = 7
NUM = 13

class AsciiCharacter():
    def __init__(self, c, t):
        self.char = c
        self.type = t

    def classify_ascii_char(self):
        if (self.type == "util"):
            if (self.char >= '0' and self.char <= '9'):
                self.type = "digit"
            elif ((self.char >= "A" and self.char <= "Z") or (self.char >= 'a' and self.char <= 'z')):
                self.type = "letter"
            else:
                self.type = "special"

class AutomatonState():
    def __init__(self, n):
        #the number of the state defined in the diagram
        self.id = n 

        #the value read
        self.read = "" 

class LexerCategorizer:
    def __init__(self, characters, a):
        # character list
        self.characters = characters
        self.automaton_state = a
        self.tokens = []
    
    def categorize(self):
        for i in range (len(self.characters)):
            next_state(char,i)

    def next_state(self,c,i):
        # if we found an "EOL" on the diagram
        if (c.type == "descartavel" or c.type == "controle"):
            if (self.automaton_state.id == INIT):
                type = "character"
            elif (self.automaton_state.id == ):
                if (read.size == 2):
                    type = "identifier"
                else:
                    type = "character"
            elif (self.automaton_state.id == 5):
                type = "int"
            elif (self.automaton_state.id == 11):
                if (read.begin == "+" or read.begin == "-"):
                    type = "snum"
                else:
                    type = "num"
            self.generate_token(type,read)

        # if current state is 1 in the diagram
        elif (self.a.id == 1):
            if (c.type == "letter"):
                reserved = self.check_reserved()
                composed = self.check_composed()
                if (not reserved and not composed):
                    a.read = a.read + c.char
                    if (characters[i+1].type == "digit"):
                        a.id = 3
                    else:
                        a.id = 4
                    
                elif (reserved):
                    pass
                elif (composed):
                    pass

            elif (c.char == "digit"):
                a.id = 4
            elif (c.char == "special"):
                a.id = 4
        
        elif (self.id == 3):
            self.generate_token("IDENTIFIER", a.red)
        
        # if current state is 4 and we're not considering buggy codes, it must be a character
        elif (self.id == 4):
            self.generate_token("CHARACTER", a.read)
        


    def check_reserved(self):
        pass
    
    def check_composed(self):
        pass
    
    def generate_token(self, type, key):
        tokens.append(Token(type, key))