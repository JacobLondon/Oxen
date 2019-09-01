from enum import Enum
from collections import OrderedDict

"""
Modify this file to change tokens and parse grammar.
"""

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

class GTok(Enum):
    # terminals
    Number      = 0
    Operator    = 1
    Ident       = 2
    # non-terminals
    Expression  = 3
    Operation   = 4

def eOperation(lhs, op, rhs):
    if op == '*':
        return lhs * rhs
    elif op == '/':
        return lhs / rhs
    elif op == '+':
        return lhs + rhs
    elif op == '-':
        return lhs - rhs
    else:
        return True

Grammar = OrderedDict({
    # terminal parsing
    GTok.Number: OrderedDict({
        (Tok.Float,):       lambda v: float(v),
        (Tok.Integer,):     lambda v: int(v),
    }),
    GTok.Operator: OrderedDict({
        (Tok.Mult,):        lambda v: str(v),
        (Tok.Divide,):      lambda v: str(v),
        (Tok.Add,):         lambda v: str(v),
        (Tok.Subtract,):    lambda v: str(v),
    }),
    # non-terminal parsing
    GTok.Expression: OrderedDict({
        (GTok.Ident,):      lambda v: str(v),
        (GTok.Number,):     lambda v: v,
    }),
    GTok.Operation: OrderedDict({
        (GTok.Expression, GTok.Operator, GTok.Expression,): lambda lhs, op, rhs: eOperation(lhs, op, rhs),
    }),
})

def strip(tokens:list):
    return list(filter(lambda t: t.tok != Tok.Whitespace, tokens))
