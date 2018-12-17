from lexer2 import Lexer
from parser import Parser
from codegen import CodeGen


###############################
#                             #
# PRIMEIRO NIVEL DE ABSTRAÇÃO #
#                             #
#     LEITURA DE ARQUIVO      #
#                             #
###############################

fname = "input.toy"
f = open(fname)
# with open(fname) as f:
#     text_input = f.read()

################################
#                              #
#  SEGUNDO NIVEL DE ABSTRAÇÃO  #
#                              #
#       CAPTURA DAS LINHAS     #
#                              #
################################

lexer = Lexer().get_lexer()
tok = []
for line in f:
    tokens = lexer.lex(line)
    for token in tokens:
        print(token)
    tok.append(tokens)

#################################
#                               #
#  TERCEIRO NIVEL DE ABSTRAÇÃO  #
#                               #
#       CARACTERES ASCII        #
#                               #
#################################

#################################
#                               #
#  TERCEIRO NIVEL DE ABSTRAÇÃO  #
#                               #
#       CARACTERES ASCII        #
#                               #
#################################



#################################
#                               #
#  SÉTIMO NIVEL DE ABSTRAÇÃO    #
#                               #
#      ANÁLISE SINTÁTICA        #
#                               #
#################################


codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)

pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
for i in range (len(tok)):
   parser.parse(tok[i]).eval()

codegen.create_ir()
codegen.save_ir("output.ll")