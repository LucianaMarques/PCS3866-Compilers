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
            next_state(i)

    def next_state(self,i):
        # if we found an "EOL" on the diagram
        if (self.characters[i].type == "descartavel" or self.characters[i].type == "controle"):
            if (self.automaton_state.id == INIT):
                self.generate_token(= "character"
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
        else:
            self.a.read = self.a.read + c.char
            if (self.a.id == 1):
                if (c.type == "letter"):
                    reserved = self.check_reserved()
                    composed = self.check_composed()
                    if (not reserved and not composed):
                        if (characters[i+1].type == "digit"):
                            self.a.id = 3
                        else:
                            self.a.id = 4
                        
                    elif (reserved):
                        pass
                    elif (composed):
                        pass

                elif (c.type == "digit"):
                    self.a.id = 4
                elif (c.type == "special"):
                    self.a.id = 4
                elif (c.char == "+" or c.char == "-"):
                    self.a.id = 5
                elif (c.char == "."):
                    self.a.id = 6
                else:
                    self.a.id = 6
            
            elif (self.a.id == 3):
                self.generate_token("IDENTIFIER", a.red)
            
            # if current state is 4 and we're not considering buggy codes, it must be a character
            elif (self.a.id == 4):
                self.generate_token("CHARACTER", a.read)

            elif (self.a.id == 5):
                self.a.id = 6
            
            elif (self.a.id == 6):
                self.a.id = 7
            
            elif (self.a.id == 7):
                if (self.characters[i+1].type == "descartavel" or self.characters[i+1] == "controle"):
                    self.generate_token("INT", self.a.read)
                elif (self.characters[i+1].type == "digit"):
                    pass
                elif (self.characters[i+1].char == "."):
                    self.a.id = 8
                else:
                    self.a.id = 9
            
            elif (self.a.id == 8):
                if (self.characters[i+1].type == "digit"):
                    pass
                else:
                    self.a.id = 9
            
            elif (self.a.id == 9):
                if (self.characters[i+1].char == "E"):
                    self.a.id = 10
                else:
                    self.a.id = 13
            
            elif (self.a.id == 10):
                self.a.id = 11

            elif (self.a.id == 11):
                self.a.id = 12
            
            elif (self.a.id == 12):
                if (self.characters[i+1].type == "digit"):
                    pass
                else:
                    self.a.id = 13
            
            elif (self.a.id == 13):
                if (self.a.read[0] == "+" or self.a.read[0] == "-"):
                    self.generate_token("SNUM", a.read)
                else:
                    self.generate_token("NUM", a.read)
      
    def check_reserved(self):
        pass
    
    def check_composed(self):
        pass
    
    def generate_token(self, type, key):
        tokens.append(Token(type, key))