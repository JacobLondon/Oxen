from enum import Enum
from collections import OrderedDict

"""
Modify this file to change tokens and parse grammar.
"""

class Tok(Enum):
    Whitespace = 0
    Identifier = 1
    Integer = 2
    Float = 3
    Add = 4
    Unknown = 5

Tokens = OrderedDict({
    Tok.Whitespace: r"[\s\t\r\n]+",
    Tok.Identifier: r"[_a-zA-Z][_a-zA-Z0-9]*",
    Tok.Float:      r"[0-9]+\.[0-9]*",
    Tok.Integer:    r"[0-9]+",
    Tok.Add:        r"\+",
    Tok.Unknown:    r".",
})

class GTok(Enum):
    Number = 0
    Expression = 1
    Operation = 2

Grammar = OrderedDict({
    GTok.Number: OrderedDict({
        (Tok.Float,): lambda v: float(v),
        (Tok.Integer,): lambda v: int(v),
    }),
    GTok.Expression: OrderedDict({
        (Tok.Identifier,): lambda v: str(v),
        (GTok.Number,): lambda v: v,
    }),
    GTok.Operation: OrderedDict({
        (GTok.Expression, Tok.Add, GTok.Expression,): lambda lhs, rhs: (lhs + rhs),
    })
})

def strip(tokens:list):
    return list(filter(lambda t: t.tok != Tok.Whitespace, tokens))
