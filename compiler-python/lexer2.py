from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()


    # Function created accordingly to the programming language's grammar
    def _add_tokens(self):
        # Reserved
        self.lexer.add('reserved', r'DATA|DEF|DIM|END|FN|FOR|GOSUB|GO TO|IF|LET|NEXT|PRINT|READ|REM|RETURN|STEP|THEN|TO')

        # End
        self.lexer.add('end', r'END')

        # Predef
        self.lexer.add('predef', r'SIN|COS|TAN|ATN|EXP|ABS|LOG|SQR|INT|RND')

        # Composed
        self.lexer.add('composed', r'FNw|GOTO|DEFFNletter|>=|<“>” | “<” “=” | Snum | ““” Character { Character } “”” | Remark .')

        # Num
        self.lexer.add('num', r'(-+)?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)')

        # Snum
        self.lexer.add('snum', r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)')

        # Integers
        self.lexer.add('int', r'\d+')

        # Digits
        self.lexer.add('digit', r'\d')

        # Identifiers
        self.lexer.add('identifier', r'\w+|\wd')

        # Letters
        self.lexer.add('letter', r'\w')

        # Character
        #self.lexer.add('character', r'\w|\d|\!|\@|\#|\&|*|\(|\)|\_|\+|\-|\=|\&|\§|\{|\[|\a|\}|\]|\°|\?|\/|\´|\`|\^|\~|\)|\<|\,|\>|\.|\:|\;|\"')

        # Print
        #self.lexer.add('PRINT', r'print')

        # Ignore spaces
        self.lexer.ignore('\s+')

        # Special chracters
        self.lexer.add('special', r'!')
        self.lexer.add('special', r'@')
        self.lexer.add('special', r'#')
        self.lexer.add('special', r'@')
        self.lexer.add('special', r'&')
        self.lexer.add('special', r'\*')
        self.lexer.add('special', r'\(')
        self.lexer.add('special', r'\)')
        self.lexer.add('special', r'_')
        self.lexer.add('special', r'\+')
        self.lexer.add('special', r'-')
        self.lexer.add('special', r'=')
        self.lexer.add('special', r'&')
        self.lexer.add('special', r'§')
        self.lexer.add('special', r'{')
        self.lexer.add('special', r'\[')
        self.lexer.add('special', r'a')
        self.lexer.add('special', r'}')
        self.lexer.add('special', r']')
        self.lexer.add('special', r'°')
        self.lexer.add('special', r'\?')
        self.lexer.add('special', r'/')
        self.lexer.add('special', r'´')
        self.lexer.add('special', r'`')
        self.lexer.add('special', r'^')
        self.lexer.add('special', r'~')
        self.lexer.add('special', r'<')
        self.lexer.add('special', r',')
        self.lexer.add('special', r'>')
        self.lexer.add('special', r'.')
        self.lexer.add('special', r':')
        self.lexer.add('special', r';')
        self.lexer.add('special', r'|')
        self.lexer.add('special', r' \ ')
        self.lexer.add('special', r'"')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
