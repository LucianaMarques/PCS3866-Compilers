from lexer2 import Lexer
from parser import Parser
from codegen import CodeGen
from llvmlite import ir, binding

# Algumas macros

int32 = ir.IntType(32)

#module_ref = ModuleRef()
codegen = CodeGen()
module = codegen.module
builder = codegen.builder
printf = codegen.printf
engine = codegen.engine

global_variables = {}


'''
Aplico a regra de int, num,
'''
def parser(tokens,builder):
    i = 0
    while(i < len(tokens)):
        j = i
        #print(tokens[j].value)
        if (tokens[j].gettokentype() == "INT"):
            j = j + 1
        # Assign - NODE 4
        if (tokens[j].value == "LET"):
            # LER O NOME DA VARIAVEL
            j += 1
            j, s = var(tokens, j)
            # PULA O '='
            j += 1
            # CALCULA VALOR DA VARIAVEL
            j, v = expression(tokens, j)
            # k = Value() 
            # k = ir.GlobalVariable(module, int32, name = s)
            # i = ir.Constant(int32,int(v))
            # global_variable.initializer = i
            # global_variables[s] = global_variable
            print("variable " + s + " value is "+v)
        elif (tokens[j].value == "READ"):
            pass
        elif (tokens[j].value == "DATA"):
            pass
        elif (tokens[j].value == "PRINT"):
            pass
        elif (tokens[j].value == "GO" or tokens[j].value == "GOTO"):
            pass
        elif (tokens[j].value == "IF"):
            pass
        elif (tokens[j].value == "FOR"):
            pass
        elif (tokens[j].value == "NEXT"):
            pass
        elif (tokens[j].value == "DIM"):
            pass
        elif (tokens[j].value == "DEF FN"):
            pass
        elif (tokens[j].value == "GOSUB"):
            pass
        elif (tokens[j].value == "REM"):
            pass

            

        #  IRBuilder.load(ptr, name='', align=None)
        #  Load value from pointer ptr. If align is passed, it should be a Python integer specifying the guaranteed pointer alignment.
        #  llvmlite.ir.GlobalVariable(module, typ, name, addrspace=0)
        # if (tokens[j].value == "PRINT"):
        #     # LER O NOME DA VARIAVEL
        #     j += 2 # pula o "
        #     j,s = var(tokens,j)
        #     j += 1 # pula o "
        #     print(s)
        #     for gv in module.global_variables:
        #         print("hey")
        #         # addr =  engine.get_global_value_address(gv.name)
        #     print('s')
        #     # value = builder.load(addr,name = s)

        i = j
        i += 1

def var(tokens, i):
    s = tokens[i].value
    #print(s)
    if (tokens[i+1].gettokentype() == "INT"):
        s = s + tokens[i+1].value
        i = i +2
    else:
        i, l = expression(tokens,i + 2)
        s = s + l
    return i, s

def expression(tokens, j):
    '''NEEDS TO RETURN A NUMBER'''
    s = ""

    # print(tokens[j].gettokentype())
    j, s = node_10(tokens, j)
    print(tokens[j].gettokentype())
    # NODE 12   
    if (tokens[j].value == "("):
        #expression(tokens,j+1) # return to node 10
        pass
    elif (tokens[j].value == "FN"):
        pass
    elif (tokens[j].value == ")"):
        pass
    return j, s

# NODE 10  
def node_10(tokens, j):
    s = ""
    if (tokens[j].value == '+'):
        s = s + tokens[j].value
        j = j+1
    elif (tokens[j].value == '-'):
        s = s + tokens[j].value
        j= j+1
    elif (tokens[j].gettokentype() == "INT"):
        s = s + tokens[j].value
        j = j + 1
    return j, s



###############################
#                             #
# PRIMEIRO NIVEL DE ABSTRAÇÃO #
#                             #
#     LEITURA DE ARQUIVO      #
#                             #
###############################

fname = "input.toy"
with open(fname) as f:
    text_input = f.read()

#print(text_input)
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
tokens = lexer.lex(text_input)
tok = []
for token in tokens:
    print(token)
    tok.append(token)

parser(tok, builder)
codegen.create_ir()
codegen.save_ir("output.ll")


# pg = Parser(module, builder, printf)

# pg.parse()
# parser = pg.get_parser()

# for token in tokens:
#     print(token)

# parser.parse(tokens).eval()

# for line in f:
#     print(line)
#     tokens = lexer.lex(line)
#     for token in tokens:
#         print(token)
#     parser.parse(tokens).eval()


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


# codegen = CodeGen()

# module = codegen.module
# builder = codegen.builder
# printf = codegen.printf

# pg = Parser(module, builder, printf)

# pg.parse()
# parser = pg.get_parser()
# parser.parse(tokens).eval()
# for i in range (len(tok)):
#    parser.parse(tok[i]).eval()
