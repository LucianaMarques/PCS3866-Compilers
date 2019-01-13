from SyntaticCateg import Token

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
        self.id = n

class LexerCategorizer:
    def __init__(self, characters, a):
        # character list
        self.characters = []
        self.automaton_state = a
        self.tokens = []
    
    def next_state(self,c,read):
        if (c.type == "descartavel" or c.type == "controle"):
            if (self.automaton_state == )
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