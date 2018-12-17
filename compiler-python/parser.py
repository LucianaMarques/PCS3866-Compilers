from rply import ParserGenerator
from ast import Number, Sum, Sub, Print, Assign


class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['reserved', 'end', 'composed', 'num', 'snum', 'int', 'digit', 'identifier', 'letter', 'special']
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
        #     if (p[1].gettokentype() == 'reserved'):
        #         if (p[1].getstr() == 'LET'):
        #             return assign(p)
        
        @self.pg.production('assign : reserved identifier special num')
        def assign(p):
            '''
            p[0] - int da coluna
            p[1] - LET
            p[2] - identifier
            p[3] - =
            p[4] - expressao
            '''
            id = p[2].getstr()
            valor = expression(p)
            return Assign(self.builder, self.module, id, valor)
        
        #@self.pg.production('Expression : { “+” | “-” } Eb { ( “+” | “-” | “*” | “/” | “” ) Eb }')
        @self.pg.production('Expression : special num')
        def expression(p):
            if(p[4].gettokentype() == 'num'):
                return float(ṕ[4].getstr())
            if(p[4].gettokentype() == 'int'):
                return int(p[4].getstr())
            else:
                return eb(p)

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

        # @self.pg.error
        # def error_handle(token):
        #     raise ValueError(token)

    def get_parser(self):
        return self.pg.build()