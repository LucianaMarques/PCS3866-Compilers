from SyntaticCateg import Token

# global variables for automaton states
IDENTIFIER = 3
CHARACTER = 4
INT = 7
NUM = 13

class AsciiCharacter():
    def __init__(self, t, c):
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
    def __init__(self):
        #the number of the state defined in the diagram
        self.id = 1

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
            self.next_state(i)

    def next_state(self,i):
        # if we found an "EOL" on the diagram
        if (self.characters[i].type == "descartavel" or self.characters[i].type == "controle"):
            if (self.automaton_state.id == 2):
                self.generate_token("INT", self.automaton_state.read)
            elif (self.automaton_state.id == 4):
                self.generate_token("CHARACTER", self.automaton_state.read)
            elif (self.automaton_state.id == 7):
                self.generate_token("INT", self.automaton_state.read)
            elif (self.automaton_state.id == 13):
                if (read.begin == "+" or read.begin == "-"):
                    self.generate_token("SNUM", self.automaton_state.read)
                else:
                    self.generate_token("NUM", self.automaton_state.read)
            elif (self.automaton_state.id == 17):
                self.generate_token("COMPOSED", self.automaton_state.read)
            # Goes back to the beginning
            self.automaton_state.id = 1

        # if current state is 1 in the diagram
        else:
            self.automaton_state.read = self.automaton_state.read + self.characters[i].char
            # print(self.automaton_state.read)
            if (self.automaton_state.id == 1):
                if (self.characters[i].type == "letter"):
                    reserved = self.check_reserved()
                    composed = self.check_composed()
                    if (not reserved and not composed):
                        if (self.characters[i+1].type == "digit"):
                            self.automaton_state.id = 3
                        else:
                            self.automaton_state.id = 4
                        
                    elif (reserved):
                        pass
                    elif (composed):
                        pass

                elif (self.characters[i].type == "digit"):
                    self.automaton_state.id = 6
                    # self.automaton_state.id = 4
                    # could be 4, check it out later
                elif (self.characters[i].type == "special"):
                    self.automaton_state.id = 4
                elif (self.characters[i].char == "+" or self.characters[i].char == "-"):
                    self.automaton_state.id = 5
                elif (self.characters[i].char == "."):
                    self.automaton_state.id = 6
                else:
                    self.automaton_state.id = 6
            
            elif (self.automaton_state.id == 3):
                self.generate_token("IDENTIFIER", self.automaton_state.read)
                self.automaton_state.id = 1
                self.automaton_state.read = ""
            
            # if current state is 4 and we're not considering buggy codes, it must be a character
            elif (self.automaton_state.id == 4):
                self.generate_token("CHARACTER", self.automaton_state.read)
                self.automaton_state.read = ""

            elif (self.automaton_state.id == 5):
                self.automaton_state.id = 6
            
            elif (self.automaton_state.id == 6):
                self.automaton_state.id = 7
            
            elif (self.automaton_state.id == 7):
                if (self.characters[i+1].type == "descartavel" or self.characters[i+1] == "controle"):
                    self.generate_token("INT", self.automaton_state.read)
                    self.automaton_state.id = 1
                    self.automaton_state.read = ""
                elif (self.characters[i+1].type == "digit"):
                    pass
                elif (self.characters[i+1].char == "."):
                    self.automaton_state.id = 8
                else:
                    self.automaton_state.id = 9
            
            elif (self.automaton_state.id == 8):
                if (self.characters[i+1].type == "digit"):
                    pass
                else:
                    self.automaton_state.id = 9
            
            elif (self.automaton_state.id == 9):
                if (self.characters[i+1].char == "E"):
                    self.automaton_state.id = 10
                else:
                    self.automaton_state.id = 13
            
            elif (self.automaton_state.id == 10):
                self.automaton_state.id = 11

            elif (self.automaton_state.id == 11):
                self.automaton_state.id = 12
            
            elif (self.automaton_state.id == 12):
                if (self.characters[i+1].type == "digit"):
                    pass
                else:
                    self.automaton_state.id = 13
            
            elif (self.automaton_state.id == 13):
                if (self.automaton_state.read[0] == "+" or self.automaton_state.read[0] == "-"):
                    self.generate_token("SNUM", automaton_state.read)
                    self.automaton_state.id = 1
                    self.automaton_state.read = ""
                else:
                    self.generate_token("NUM", self.automaton_state.read)
                    self.automaton_state.id = 1
                    self.automaton_state.read = ""
            
            else:
                pass
      
    def check_reserved(self):
        pass
    
    def check_composed(self):
        pass
    
    def generate_token(self, type, key):
        self.tokens.append(Token(type, key))