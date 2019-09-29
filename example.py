from collections import OrderedDict
from enum import Enum
from lexer import Lexer

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
    def __init__(self):
        Lexer.__init__(self, Tokens)

    def strip(self, tokens: list):
        return list(filter(lambda t: t.tok != Tok.Whitespace, tokens))