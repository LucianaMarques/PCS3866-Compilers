from queue import Queue
from LexerCateg import AsciiCharacter, LexerCategorizer, AutomatonState

class MotorDeEventos():
    def __init__(self):
        self.q = Queue()
        # inicializa fila de eventos com "Inicio"
        self.q.put(Evento("inicio", None))

        # Lista de tokens  
        self.characters = [] 
        self.tokens = []

    def event_extraction(self):
        if (self.q.empty()):
            return 
        else:
            return self.q.get()

    def add_event(self, e):
        self.q.put(e)
    
    def current_event(self, e):
        if (e.type == "inicio"):
            print("INICIO MOTOR DE EVENTOS")
        elif (e.type == "extrair_linhas"):
            print("INICIO LEITURA DO ARQUIVO FONTE")
            arquivo = e.value
            f = open(arquivo, 'r')
            for line in f:
                line_event = Evento("extrair_caracteres", line)
                self.add_event(line_event)
        elif (e.type == "extrair_caracteres"):
            print("LINHA LIDA")
            for each in e.value:
                self.add_event(Evento("classificar_caracter",each))
                # print(each)
        elif (e.type == "classificar_caracter"):
            print("CLASSIFICAÇÃO DE CARACTERES")
            if (e.value == " "):
                t = "descartavel"
            elif (e.value == '\n'):
                t = "controle"
            else:
                t = "util"
            self.characters.append(AsciiCharacter(t,e.value))
            self.add_event(Evento("reclassificar_caracteres", self.tokens))
        elif(e.type == "reclassificar_caracteres"):
            print("CLASSIFICAÇÃO LÉXICA")
            for char in self.characters:
                char.classify_ascii_char()
                # print(char.char)
            self.add_event(Evento("extrair_tokens", self.tokens))
        elif (e.type == "extrair_tokens"):
            print("EXTRAÇÃO DE TOKENS")
            # s = ""
            # for token in self.tokens:
            #     if (token.type != "descartavel"):
            #         s = s + token.key
            #         if (token.type == "letter"):
            #             #decidir se é identifier, character, composed ou reserved
            #             pass
            automatonState = AutomatonState()
            lexCateg = LexerCategorizer(self.characters,automatonState)
            lexCateg.categorize()
            tokens2 = lexCateg.tokens
            print(len(tokens2))
                      
    def event_cycle(self):
        while (self.q.empty() == False):
            e = self.event_extraction()
            self.current_event(e)


class Evento():
    def __init__(self, t, v):
        self.type = t
        self.value = v