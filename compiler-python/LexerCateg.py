from SyntaticCateg import Token

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
        i = 0 
        while (i < len(self.characters)):
            proximo = self.next_state(i)
            i += proximo

    def next_state(self,i):
        proximo = 1
        self.automaton_state.read = self.automaton_state.read + self.characters[i].char
        if (self.automaton_state.id == 1):
            if (self.characters[i].type == "letter"):
                # check if end of characters
                if (i != len(self.characters) - 1):
                    reserved, extra = self.check_reserved(i)
                # if end of characters, no way that it's reserved
                else:
                    reserved = False
                    extra = ''
                if (not reserved):
                    # Identifier
                    if (self.characters[i+1].type == "digit"):
                        self.generate_token("IDENTIFIER", self.automaton_state.read)
                        proximo = 2
                        self.automaton_state.read = ""
                        self.automaton_state.id = 1
                    else:
                        self.generate_token("CHARACTER", self.characters[i].char)
                        self.automaton_state.read = ""
                        self.automaton_state.id = 1
                else:
                    self.automaton_state.read = self.automaton_state.read + extra
                    self.generate_token("RESERVED", self.automaton_state.read)
                    self.automaton_state.read = ""
                    self.automaton_state.id = 1
                    proximo = len(extra) + 1

            elif (self.characters[i].type == "special"):
                if (self.characters[i].char == "+" or self.characters[i].char == "-"):
                    if (self.characters[i+1].type == "digit"):
                        self.automaton_state.id = 5
                    else:
                        self.generate_token("CHARACTER", self.automaton_state.read)
                        self.automaton_state.id = 1
                        self.automaton_state.read = ""
                elif (self.characters[i].char == "."):
                    self.automaton_state.id = 6
                else:
                    self.generate_token("CHARACTER",self.characters[i].char)
                    self.automaton_state.id = 1
                    self.automaton_state.read = ""

            elif (self.characters[i].type == "digit"):
                if (self.characters[i+1].type != "digit" and self.characters[i+1].char != "." and self.characters[i+1].char != "E"):
                    self.generate_token("INT", self.automaton_state.read)
                    self.automaton_state.id = 1
                    self.automaton_state.read = ""
                else:
                    self.automaton_state.id = 7

            elif (self.characters[i].type == "controle"):
                self.generate_token("EOL", "")
            
            elif (self.characters[i].type == "descartavel"):
                self.automaton_state.read = ""

        elif (self.automaton_state.id == 5):
            self.automaton_state.id = 6
        
        elif (self.automaton_state.id == 6):
            self.automaton_state.id == 7

        elif (self.automaton_state.id == 7):
            if (self.characters[i].type == "digit"):
                self.automaton_state.id = 7
            elif (self.characters[i].type == "descartavel" or self.characters[i].type == "controle"):
                self.generate_token("INT", self.characters[i].char)
                self.automaton_state.id = 1
                self.automaton_state.read = ""
                if (self.characters[i].type == "controle"):
                    self.generate_token("EOL", "")
            elif(self.characters[i].char == "."):
                self.automaton_state.id = 8
            else:
                self.automaton_state.id = 9
        
        elif(self.automaton_state.id == 8):
            if (self.characters[i+1].type == "digit"):
                self.automaton_state.id = 8
            elif (self.characters[i].char == "E"):
                self.automaton_state.id = 9
            else:
                if (self.automaton_state.read[0] == "+" or self.automaton_state.read[0] == "-"):
                    self.generate_token("SNUM", self.automaton_state.read)
                else:
                    self.generate_token("NUM", self.automaton_state.read)
                self.automaton_state.id = 1
                self.automaton_state.read = ""
        
        elif(self.automaton_state.id == 9):
            if (self.characters[i].char == "E"):
                j = i
                if (self.characters[i+1].char[0] == "+" or self.characters[i+1].char[0] == "-"):
                    self.automaton_state.read = self.automaton_state.read + self.characters[i].char
                    j += 2
                else:
                    j += 1
                while (self.characters[j].type == "digit"):
                    self.automaton_state.read = self.automaton_state.read + self.characters[i].char
                    j += 1
                proximo = j - i
            if (self.automaton_state.read[0] == "+" or self.automaton_state.read[0] == "-"):
                self.generate_token("SNUM", self.automaton_state.read)
            else:
                self.generate_token("NUM", self.automaton_state.read)
            self.automaton_state.id = 1
            self.automaton_state.read = ""
        return proximo
      
    # Check for RESERVED type token
    def check_reserved(self, i):
        print("CHECKING IF RESERVED")
        #“ABS” | “ATN” 
        if (self.characters[i].char == 'A'):
            if (self.characters[i+1].char == 'B'):
                return True, 'BS'
            elif(self.characters[i+1].char == 'T'):
                return True, 'TN'
            else:
                return False, ''
        elif (self.characters[i].char == 'C'):
            if (self.characters[i+1] == 'O'):
                return True, 'OS'
            else:
                return False, ''
        #“DATA” | “DEF” | “DIM” 
        elif (self.characters[i].char == 'D'):
            if (self.characters[i+1].char == 'A'):
                return True, 'ATA'
            elif (self.characters[i+1].char == 'E'):
                return True, 'EF'
            elif (self.characters[i+1].char == 'I'):
                return True, 'IM'
            else:
                return False, ''
        # “END” |“EXP”
        elif (self.characters[i].char == 'E'):
            if (self.characters[i+1].char == 'N'):
                return True, 'ND'
            elif (self.characters[i+1].char == 'X'):
                return True, 'XP'
            else:
                return False, ''
        # “FN” |“FOR”
        elif (self.characters[i].char == 'F'):
            if (self.characters[i+1].char == 'N'):
                return True, 'N'
            elif (self.characters[i+1].char == 'O'):
                return True, 'OR'
            else:
                return False, ''
        # “GO” | “GOSUB” | “GOTO”
        elif (self.characters[i].char == 'G'):
            if (self.characters[i+2].char == 'S'):
                return True, 'OSUB'
            elif (self.characters[i+2].char == 'T'):
                return True, 'OTO'
            elif (self.characters[i+1].char == 'O'):
                return True, 'O'
            else:
                return False, ''
        # “IF” |“INT”
        elif (self.characters[i].char == 'I'):
            if (self.characters[i+1].char == 'F'):
                return True, 'F'
            elif (self.characters[i+1].char == 'N'):
                return True, 'NT'
            else:
                return False, ''    
        # “LET” | “LOG”
        elif (self.characters[i].char == 'L'):
            if (self.characters[i+1].char == 'E'):
                return True, 'ET'
            elif (self.characters[i+1].char == 'O'):
                return True, 'OG'
            else:
                return False, ''
        # "NEXT"
        elif (self.characters[i].char == 'N'):
            print("hey, found an N")
            if (self.characters[i+1].char == 'E'):
                return True, 'EXT'
            else:
                return False, ''
        # "PRINT"
        elif (self.characters[i].char == 'P'):
            if (self.characters[i+1].char == 'R'):
                return True, 'RINT'
            else:
                return False, ''
        # “READ” |“REM” | “RETURN” | “RND”
        elif (self.characters[i].char == 'R'):
            if (self.characters[i+1].char == 'N'):
                return True, 'ND'
            elif (self.characters[i+2].char == 'A'):
                return True, 'EAD'
            elif (self.characters[i+2].char == 'T'):
                return True, 'ETURN'
            elif (self.characters[i+2].char == 'M'):
                return True, 'EM'
            else:
                return False, ''
        # “SIN” |“SQR” |“STEP”
        elif (self.characters[i].char == 'S'):
            if (self.characters[i+1].char == 'I'):
                return True, 'IN'
            elif (self.characters[i+1].char == 'Q'):
                return True, 'QR'
            elif (self.characters[i+1].char == 'T'):
                return True, 'TEP'
            else:
                return False, ''
        # “TAN” | “THEN” | “TO”
        elif (self.characters[i].char == 'T'):
            if (self.characters[i+1].char == 'A'):
                return True, 'AN'
            elif (self.characters[i+1].char == 'H'):
                return True, 'HEN'
            elif (self.characters[i+1].char == 'O'):
                return True, 'O'
            else:
                return False, ''
        else:
            return False, ''
    
    def generate_token(self, type, key):
        self.tokens.append(Token(type, key))
        print("generated token ", type, key)