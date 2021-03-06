from queue import Queue
from LexerCateg import AsciiCharacter, LexerCategorizer, AutomatonState
from SyntaticCateg import Token, Parser

# Parser
parser = Parser()

class Evento():
    def __init__(self, t, v):
        self.type = t
        self.value = v

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
                # Ignore remark lines
                if (line[4:7] != 'REM'):
                    print("LINHA LIDA")
                    self.add_event(Evento("extrair_caracteres", line))
        
        elif (e.type == "extrair_caracteres"):
            print("CLASSIFICAÇÃO DE CARACTERES")
            for each in e.value:
                self.add_event(Evento("classificar_caracter",each))
                # print(each)

        elif (e.type == "classificar_caracter"):
            if (e.value == " "):
                t = "descartavel"
            elif (e.value == '\n'):
                t = "controle"
            else:
                t = "util"
            self.characters.append(AsciiCharacter(t,e.value))
            if (self.q.qsize() == 0):
                self.add_event(Evento("reclassificar_caracteres", self.tokens))

        elif(e.type == "reclassificar_caracteres"):
            print("CLASSIFICAÇÃO LÉXICA")
            for char in self.characters:
                char.classify_ascii_char()
            self.add_event(Evento("extrair_tokens", self.tokens))

        elif (e.type == "extrair_tokens"):
            print("EXTRAÇÃO DE TOKENS")
            # Categorizador Léxico - autômato
            automatonState = AutomatonState()
            lexCateg = LexerCategorizer(self.characters,automatonState)
            lexCateg.categorize()
            tokens2 = lexCateg.tokens
            self.add_event(Evento("recategorizar_tokens", tokens2))
        
        elif (e.type == "recategorizar_tokens"):
            print("RECATEGORIZAR TOKENS")
            parser.tokens = e.value
            parser.recategorize_tokens()
            for token in parser.tokens:
                print("Token: ",token.type,token.key)
            self.add_event(Evento("extrair_sintaxes", parser))
        
        elif (e.type == "extrair_sintaxes"):
            print("EXTRAÇÃO DE SINTAXES")
            parser.syntax_extraction()
            self.add_event(Evento("geracao_codigo", parser.sintaxes))
        
        elif (e.type == "geracao_codigo"):
            print("CODIGO GERADO")
            self.add_event(Evento("fim", ""))
        
        elif (e.type == "fim"):
            print("FIM DE COMPILAÇÃO")

    def event_cycle(self):
        while (self.q.empty() == False):
            e = self.event_extraction()
            self.current_event(e)