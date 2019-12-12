from collections import OrderedDict
from enum import Enum, unique
from lexer import Lexer, Token
from typing import List

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
    LParen      = 8
    RParen      = 9

Definitions = OrderedDict({
    Tok.Whitespace: r"[\s\t\r\n]+",
    Tok.Float:      r"[0-9]+\.[0-9]*",
    Tok.Integer:    r"[0-9]+",
    Tok.LParen:     r"\(",
    Tok.RParen:     r"\)",
    Tok.Mult:       r"\*",
    Tok.Divide:     r"\/",
    Tok.Add:        r"\+",
    Tok.Subtract:   r"-",
    Tok.Unknown:    r".",
})

"""

"""

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.index = 0
        self.curr = None
        self.result: str = ""
    
    def eat(self, sub):
        print(self.curr)
        self.result += str(sub)
        if self.index < len(self.tokens):
            self.curr = self.tokens[self.index]
            self.index += 1

    # factor: (INTEGER | FLOAT) | (LPAREN expr RPAREN)
    def factor(self):
        if self.curr.cmp(Tok.Float):
            self.eat(self.curr.value)
        elif self.curr.cmp(Tok.Integer):
            self.eat(self.curr.value)
        elif self.curr.cmp(Tok.LParen):
            self.eat("(")
            self.expr()
            self.eat(")")

    # term: factor((MUL | DIV) factor)*
    def term(self):
        self.factor()
        if self.curr.cmp(Tok.Mult):
            self.eat("*")
            self.factor()
        elif self.curr.cmp(Tok.Divide):
            self.eat("/")
            self.factor()

    # term((PLUS | MINUS) term)*
    def expr(self):
        self.term()
        if self.curr.cmp(Tok.Add):
            self.eat("+")
            self.term()
        elif self.curr.cmp(Tok.Subtract):
            self.eat("-")
            self.term()

    def read(self):
        self.eat("")
        self.expr()
    
if __name__ == '__main__':
    l = Lexer(Definitions)
    l.read("10 * 5.1").lex().strip(Tok.Whitespace)
    print(l.tokens)
    p = Parser(l.tokens)
    p.read()
    print(p.result)
