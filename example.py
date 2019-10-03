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

if __name__ == '__main__':
    l = Lexer(Tokens)
    l.lex("10 * 5 is 50.").strip(Tok.Whitespace)
    print(l.tokenized)
