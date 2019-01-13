from rply import ParserGenerator
from ast import Number, Sum, Sub, Print, Assign


class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['RESERVED', 'END', 'DIGIT', 'LETTER', 'SPECIAL']
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        # @self.pg.production('program: BStatement')
        # def program(p):
        #     return bstatement(p)

        # @self.pg.production('Bstatement: int ( Assign | Read | Data | Print | Goto | If | For | Next | Dim | Def | Gosub | Return | Remark ) .')
        # def bstatement(p):
        #     if (p[1].gettokentype() == 'RESERVED'):
        #         if (p[1].getstr() == 'LET'):
        #             return assign(p)
        
        @self.pg.production('program : int bstatement int END')
        def program(p):
            print("Found a program")
            return BStatement(self.builder, self.module)

        @self.pg.production('bstatement : int assign')
        @self.pg.production('bstatement : int read')
        @self.pg.production('bstatement : int data')
        @self.pg.production('bstatement : int print')
        @self.pg.production('bstatement : int goto')
        @self.pg.production('bstatement : int if')
        @self.pg.production('bstatement : int for')
        @self.pg.production('bstatement : int next')
        @self.pg.production('bstatement : int dim')
        @self.pg.production('bstatement : int def')
        @self.pg.production('bstatement : int gosub')
        @self.pg.production('bstatement : int return')
        @self.pg.production('bstatement : int remark')
        @self.pg.production('bstament : bstatement bstatement')
        def bstament(p):
            print("Found a bstatement")


        @self.pg.production('assign : RESERVED var SPECIAL expression')
        def assign(p):
            '''
            p[0] - LET
            p[1] - variable name
            p[2] - =
            p[3] - expressao
            '''
            id = p[1].getstr()
            valor = expression(p)
            return Assign(self.builder, self.module, id, valor)

        @self.pg.production('var : LETTER num')
        def var(p):
            s  = p[0].value + p[1].value
            return Var(self.builder, self.module, s)

        @self.pg.production('expression : SPECIAL eb')
        @self.pg.production('expression : eb')
        @self.pg.production('expression : eb SPECIAL eb')
        @self.pg.production('expression : SPECIAL eb SPECIAL eb')
        def expression(p):
            return
        
        @self.pg.production('eb : num')
        @self.pg.production('eb : var')
        @self.pg.production('eb : SPECIAL expression SPECIAL')
        @self.pg.production('eb : RESERVED LETTER SPECIAL expression SPECIAL')
        @self.pg.production('eb : predef SPECIAL expression SPECIAL')
        def eb(p):
            if (p[0].gettokentype() == 'DIGIT'):   return
            elif (p[0].gettokentype() == 'LETTER'):
                return
            else:
                return        
        
        @self.pg.production('read : RESERVED var')
        @self.pg.production('read : RESERVED var SPECIAL var')
        def read(p):
            return

        @self.pg.production('data : RESERVED snum')
        @self.pg.production('data : RESERVED snum SPECIAL snum')
        def data(p):
            return

        @self.pg.production('print : RESERVED printitem SPECIAL')
        @self.pg.production('print : RESERVED printitem SPECIAL printitem SPECIAL')
        def print(p):
            '''
            P[0] - int da linha
            p[1] - PRINT
            p[2] - inteiro ou nome de uma variavel 
            '''
            Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('printitem : expression')
        @self.pg.production('printitem : SPECIAL character SPECIAL expression')
        def printitem(p):
            '''
            p[0] = numero ou variavel
            '''
            if (p[0].gettokentype() == 'num'):
                return Number(self.builder, self.module, int(p[0].value))
            else:
                return PrintItem(self.builder, self.module, p[0])

        @self.pg.production('goto : RESERVED int')
        def goto(p):
            return

        @self.pg.production('if : RESERVED expression SPECIAL expression RESERVED int')
        def if_function(p):
            return
    
        @self.pg.production('for : RESERVED LETTER DIGIT spon RESERVED expression RESERVED expression')
        def for_function(p):
            return

        @self.pg.production('next : RESERVED LETTER DIGIT')
        def next(p):
            return

        @self.pg.production('dim : RESERVED LETTER SPECIAL int SPECIAL')
        @self.pg.production('dim : RESERVED LETTER SPECIAL int SPECIAL int SPECIAL')
        @self.pg.production('dim : RESERVED LETTER SPECIAL int SPECIAL SPECIAL LETTER SPECIAL int SPECIAL int SPECIAL')
        @self.pg.production('dim : RESERVED LETTER SPECIAL int SPECIAL int SPECIAL SPECIAL LETTER eSPECIAL int int SPECIAL int eSPECIAL')
        def dim(p):
            return

        @self.pg.production('def : RESERVED RESERVED LETTER SPECIAL LETTER DIGIT spexpression')
        def def_function(p):
            return
        
        @self.pg.production('gosub : RESERVED int')
        def gosub(p):  
            return   
        
        @self.pg.production('return : RESERVED')
        def return_function(p):
            return 

        @self.pg.production('remark : character')
        def remark(p):    
            '''
            comentario
            '''
            return Remark()

        @self.pg.production('int : int int')
        @self.pg.production('int : DIGIT')
        def int_function(p):
            result = 0
            for i in range(len(p)):
                result = result*10 + p[i]
            return Number(self.builder, self.module, result)
        
        @self.pg.production('num : int SPECIAL int')
        @self.pg.production('num : SPECIAL int')
        def num(p):
            value = 0
            if (p[0].gettokentype() == 'SPECIAL'):
                value = p[1].value/10000
            else:
                value = p[0].value + p[2]/10000
            
            return Number(self.builder, self.module, value)

        @self.pg.production('num : SPECIAL num')
        def snum(p):
            value = p[1].value
            if (p[0].getstr() == '-'):
                value = value*(-1)
            return Number(self.builder, self.module, value)

        @self.pg.production('charater : LETTER')
        @self.pg.production('charater : DIGIT')
        @self.pg.production('charater : SPECIAL')
        @self.pg.production('character : character character')
        def charater(p):
            return Character(p[0].value)

        
        #@self.pg.production('Expression : { “+” | “-” } Eb { ( “+” | “-” | “*” | “/” | “” ) Eb }')
        # @self.pg.production('Expression : SPECIAL num')
        # def expression(p):
        #     if(p[4].gettokentype() == 'num'):
        #         return float(ṕ[4].getstr())
        #     if(p[4].gettokentype() == 'int'):
        #         return int(p[4].getstr())
        #     else:
        #         return eb(p)

        # @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        # def program(p):
        #     return Print(self.builder, self.module, self.printf, p[2])

        # @self.pg.production('expression : expression SUM expression')
        # @self.pg.production('expression : expression SUB expression')
        # def expression(p):
        #     left = p[0]
        #     right = p[2]
        #     operator = p[1]
        #     if operator.gettokentype() == 'SUM':
        #         return Sum(self.builder, self.module, left, right)
        #     elif operator.gettokentype() == 'SUB':
        #         return Sub(self.builder, self.module, left, right)

        # @self.pg.production('expression : NUMBER')
        # def number(p):
        #     return Number(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()