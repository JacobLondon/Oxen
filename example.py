from collections import OrderedDict
from lexer import Lexer, Token, Syms
from typing import List

table = Syms([
    "Whitespace",
    "Float",
    "Integer",
    "Mult",
    "Divide",
    "Add",
    "Subtract",
    "LParen",
    "RParen",
    "Unknown",
])

Definitions = OrderedDict({
    table.Whitespace: r"[\s\t\r\n]+",
    table.Float:      r"[0-9]+\.[0-9]*",
    table.Integer:    r"[0-9]+",
    table.LParen:     r"\(",
    table.RParen:     r"\)",
    table.Mult:       r"\*",
    table.Divide:     r"\/",
    table.Add:        r"\+",
    table.Subtract:   r"-",
    table.Unknown:    r".",
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
        if self.curr.cmp(table.Float):
            self.eat(self.curr.value)
        elif self.curr.cmp(table.Integer):
            self.eat(self.curr.value)
        elif self.curr.cmp(table.LParen):
            self.eat("(")
            self.expr()
            self.eat(")")

    # term: factor((MUL | DIV) factor)*
    def term(self):
        self.factor()
        if self.curr.cmp(table.Mult):
            self.eat("*")
            self.factor()
        elif self.curr.cmp(table.Divide):
            self.eat("/")
            self.factor()

    # term: ((PLUS | MINUS) term)*
    def expr(self):
        self.term()
        if self.curr.cmp(table.Add):
            self.eat("+")
            self.term()
        elif self.curr.cmp(table.Subtract):
            self.eat("-")
            self.term()

    def read(self):
        self.eat("")
        self.expr()
    
if __name__ == '__main__':
    l = Lexer(Definitions)
    l.read("10 * 5.1").lex().strip(table.Whitespace)
    print(l.tokens)
    p = Parser(l.tokens)
    p.read()
    print(p.result)
