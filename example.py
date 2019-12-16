from collections import OrderedDict
from lexer import Lexer, Token, Syms
from typing import List

table = Syms([
    "Whitespace",
    "If",
    "Id",
    "Float",
    "Integer",
    "LCurly",
    "RCurly",
    "LParen",
    "RParen",
    "Assign",
    "Mult",
    "Divide",
    "Add",
    "Subtract",
    "Unknown",
])

Definitions = OrderedDict({
    table.Whitespace: r"[\s\t\r\n]+",
    table.If:         r"if",
    table.Id:         r"[a-zA-Z_][a-zA-Z0-9_]*",
    table.Float:      r"[0-9]+\.[0-9]*",
    table.Integer:    r"[0-9]+",
    table.LCurly:     r"{",
    table.RCurly:     r"}",
    table.LParen:     r"\(",
    table.RParen:     r"\)",
    table.Assign:     r"=",
    table.Mult:       r"\*",
    table.Divide:     r"\/",
    table.Add:        r"\+",
    table.Subtract:   r"-",
    table.Unknown:    r".",
})

"""
Productions:
block  : LCurly stmts RCurly
stmts  : stmts stmt | stmt
stmt   : Id Assign expr | If LParen expr RParen block
expr   : term Add term | term Sub term
term   : factor Mult factor | factor Divide factor
factor : Id | Float | Integer | LParen expr RParen
"""

def error(*msg):
    print(*msg)
    exit(-1)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.index = 0
        self.curr = None
        self.result: str = ""
        self.done = False
    
    def eat(self, sub):
        print(self.curr)
        if self.curr is not None and sub != self.curr.value:
            print(f"\n{self.curr.lineno}:{self.curr.colno}: Expected '{sub}' but found '{self.curr.value}'")
            exit(-1)
        self.result += str(sub)
        if self.index < len(self.tokens):
            self.curr = self.tokens[self.index]
            self.index += 1
        else:
            self.done = True

    # factor: (INTEGER | FLOAT) | (LPAREN expr RPAREN)
    def factor(self):
        if self.curr.cmp(table.Id):
            self.eat(self.curr.value)
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

    def stmt(self):
        if self.curr.cmp(table.Id):
            self.eat(self.curr.value)

            # variable assignment
            if self.curr.cmp(table.Assign):
                self.eat("=")
                self.expr()
                self.eat(";")
        
        # if statement
        elif self.curr.cmp(table.If):
            self.eat("if")
            self.eat("(")
            self.expr()
            self.eat(")")
            self.block()

        # invalid symbol
        else:
            print(f"{self.curr.lineno}:{self.curr.colno}: Unexpected symbol '{self.curr.value}'")
            exit(-1)

    def stmts(self):
        while self.curr is not None and not self.curr.cmp(table.RCurly) and not self.done:
            self.stmt()

    def block(self):
        if self.curr.cmp(table.LCurly):
            self.eat("{")
            self.stmts()
            self.eat("}")

    def read(self):
        self.eat("")
        self.stmts()
    
if __name__ == '__main__':
    l = Lexer(Definitions)
    l.read("if (5 + 1) {a = 5;}").lex().strip(table.Whitespace)
    print(l.tokens)
    p = Parser(l.tokens)
    p.read()
    print(p.result)
