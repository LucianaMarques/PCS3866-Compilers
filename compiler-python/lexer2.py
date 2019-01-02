from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()


    # Function created accordingly to the programming language's grammar
    def _add_tokens(self):
        # Reserved
        self.lexer.add('RESERVED', r'DATA|DEF|DIM|END|FN|FOR|GOSUB|GO TO|IF|LET|NEXT|PRINT|READ|REM|RETURN|STEP|THEN|TO')

        # End
        self.lexer.add('END', r'END')

        # Predef
        self.lexer.add('PREDEF', r'SIN|COS|TAN|ATN|EXP|ABS|LOG|SQR|INT|RND')

        # Composed
        #self.lexer.add('COMPOSED', r'FNw|GOTO|DEFFNletter|>=|<“>” | “<” “=” | Snum | ““”w+“”” | ““”d+“””| ““”wd+“””““”w+“””Remark .')

        # Num
        self.lexer.add('NUM', r'(-+)?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)')

        # Snum
        # self.lexer.add('snum', r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)')

        # Integers
        self.lexer.add('INT', r'\d+')

        # Digits
        self.lexer.add('DIGIT', r'\d')

        # Identifiers
        # self.lexer.add('identifier', r'\w+|\wd')

        # Letters
        self.lexer.add('LETTER', r'\w')

        # Character
        #self.lexer.add('character', r'\w|\d|\!|\@|\#|\&|*|\(|\)|\_|\+|\-|\=|\&|\§|\{|\[|\a|\}|\]|\°|\?|\/|\´|\`|\^|\~|\)|\<|\,|\>|\.|\:|\;|\"')

        # Print
        #self.lexer.add('PRINT', r'print')

        # Ignore spaces
        self.lexer.ignore('\s+')

        #Equal
        self.lexer.add('EQUAL', r'=')

        # Special chracters
        self.lexer.add('SPECIAL', r'!')
        self.lexer.add('SPECIAL', r'@')
        self.lexer.add('SPECIAL', r'#')
        self.lexer.add('SPECIAL', r'@')
        self.lexer.add('SPECIAL', r'&')
        self.lexer.add('SPECIAL', r'\*')
        self.lexer.add('SPECIAL', r'\(')
        self.lexer.add('SPECIAL', r'\)')
        self.lexer.add('SPECIAL', r'_')
        self.lexer.add('SPECIAL', r'\+')
        self.lexer.add('SPECIAL', r'-')
        self.lexer.add('SPECIAL', r'&')
        self.lexer.add('SPECIAL', r'§')
        self.lexer.add('SPECIAL', r'{')
        self.lexer.add('SPECIAL', r'\[')
        self.lexer.add('SPECIAL', r'a')
        self.lexer.add('SPECIAL', r'}')
        self.lexer.add('SPECIAL', r']')
        self.lexer.add('SPECIAL', r'°')
        self.lexer.add('SPECIAL', r'\?')
        self.lexer.add('SPECIAL', r'/')
        self.lexer.add('SPECIAL', r'´')
        self.lexer.add('SPECIAL', r'`')
        self.lexer.add('SPECIAL', r'^')
        self.lexer.add('SPECIAL', r'~')
        self.lexer.add('SPECIAL', r'<')
        self.lexer.add('SPECIAL', r',')
        self.lexer.add('SPECIAL', r'>')
        self.lexer.add('SPECIAL', r'.')
        self.lexer.add('SPECIAL', r':')
        self.lexer.add('SPECIAL', r';')
        self.lexer.add('SPECIAL', r'|')
        self.lexer.add('SPECIAL', r' \ ')
        self.lexer.add('SPECIAL', r'"')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
