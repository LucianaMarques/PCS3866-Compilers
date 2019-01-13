from SyntaticCateg import Token

# global variables for automaton states
INIT = 1


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
        self.characters = []
        self.automaton_state = a
        self.tokens = []
    
    def next_state(self,c,read):
        if (c.type == "descartavel" or c.type == "controle"):
            if (self.automaton_state.id == 1):
                type = "character"
            elif (self.automaton_state.id == 2):
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
        elif (self.a.id == 1):
            if (c.char == "letter"):
                reserved = self.check_reserved()
                composed = self.check_composed()
                if (reserved):

            elif (c.char == "digit"):
                pass
            elif (c.char == "special"):
                pass
    
    def check_reserved(self):
        pass
    
    def check_composed(self):
        pass
    
    def generate_token(self, read):
        tokens.append(Token(read))