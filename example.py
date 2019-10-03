from collections import OrderedDict
from enum import Enum, unique
from lexer import Lexer

@unique
class Tok(Enum):
    Whitespace  = 0
    Float       = 1
    Mult        = 2
    Divide      = 3
    Integer     = 4
    Add         = 5
    Subtract    = 6
    Unknown     = 7

Tokens = OrderedDict({
    Tok.Whitespace: r"[\s\t\r\n]+",
    Tok.Float:      r"[0-9]+\.[0-9]*",
    Tok.Mult:       r"\*",
    Tok.Divide:     r"\/",
    Tok.Integer:    r"[0-9]+",
    Tok.Add:        r"\+",
    Tok.Subtract:   r"-",
    Tok.Unknown:    r".",
})

class MyLexer(Lexer):
    def __init__(self, tokens):
        Lexer.__init__(self, tokens)

    def strip(self, token: Tok):
        self.tokenized = list(filter(lambda t: t.tok != token, self.tokenized))
        return self

if __name__ == '__main__':
    l = MyLexer(Tokens)
    l.lex("10 * 5 is 50.").strip(Tok.Whitespace)
    print(l.tokenized)
