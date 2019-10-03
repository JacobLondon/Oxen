from collections import OrderedDict
import copy
from enum import Enum, unique
import re
from typing import List

# overwritten by user
@unique
class Tok(Enum):
    pass
Tokens: OrderedDict = None

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
        self.text: str = ""
        self.tokens: OrderedDict = tokens
        self.tokenized: List[Token] = []

    def read(self, text: str):
        self.text = text
        return self

    def fread(self, filename: str):
        with open(filename, 'r') as input_file:
            self.read(input_file.read())
        return self

    def lex(self):
        lineno = 0
        colno  = 0
        text = copy.deepcopy(self.text)
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
                # regex was the next item (next starts at index 0), so match
                matched = True
                if '\n' in text[start:end]:
                    lineno += text[start:end].count('\n')
                    colno = len(text[start:end]) - text[start:end].rfind('\n')
                else:
                    colno += end
                # record token
                self.tokenized.append(Token(tok, text[start:end]))
                text = text[end:]
                break
            # ensure no infinite loop
            if not matched:
                print(f"Unexpected token on line {lineno}:{colno}:\n\t'{text[:start]}'")
                exit(-1)
        return self

    def strip(self, token: Tok):
        self.tokenized = list(filter(lambda t: t.tok != token, self.tokenized))
        return self

    def find(self, pattern: List[Tok]) -> int:
        for i, _ in enumerate(self.tokenized):
            tokens = [t.tok for t in self.tokenized]
            if tokens[i:i+len(pattern)] == pattern:
                return i
