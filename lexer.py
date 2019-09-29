from collections import OrderedDict
from enum import Enum
import re
from typing import List

class Token:
    def __init__(self, tok, value):
        self.tok = tok
        self.value = value
    def __str__(self):
        return f"{self.tok}({self.value})"
    def __repr__(self):
        return self.__str__()

class Lexer:

    def __init__(self, tokens: OrderedDict):
        self.tokens: OrderedDict = tokens
        self.tokenized: List[Token] = []

    def lex(self, text: str) -> list:
        while text:
            matched = False
            for tok, reg in self.tokens.items():
                # look for the token with the next highest priority
                found = re.search(reg, text)
                if not found:
                    continue
                # start / end indices of token
                start, end = found.span()
                if start != 0:
                    continue
                matched = True
                # record token
                self.tokenized.append(Token(tok, text[start:end]))
                text = text[end:]
                break
            # ensure no infinite loop
            if not matched:
                print(f"Failure to tokenize:\n{text}")
                exit(-1)
        return self.tokenized
