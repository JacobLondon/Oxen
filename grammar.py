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
    # terminals
    Number = 0
    Operator = 1
    Ident = 2
    # non-terminals
    Expression = 3
    Operation = 4

Grammar = OrderedDict({
    # terminal parsing
    GTok.Number: OrderedDict({
        (Tok.Float,): lambda v: float(v),
        (Tok.Integer,): lambda v: int(v),
    }),
    GTok.Operator: OrderedDict({
        (Tok.Add,): lambda v: str(v),
    }),
    GTok.Ident: OrderedDict({
        (Tok.Identifier,): lambda v: str(v),
    }),
    # non-terminal parsing
    GTok.Expression: OrderedDict({
        (GTok.Ident,): lambda v: str(v),
        (GTok.Number,): lambda v: v,
    }),
    GTok.Operation: OrderedDict({
        (GTok.Expression, GTok.Operator, GTok.Expression,): lambda lhs, op, rhs: (lhs + rhs),
    }),
})

def strip(tokens:list):
    return list(filter(lambda t: t.tok != Tok.Whitespace, tokens))
