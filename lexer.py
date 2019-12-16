from collections import OrderedDict
import copy
import re
from typing import List

# added to by user
class Syms:
    def __init__(self, symbols: List[str]):
        self.lookup = {}
        for i, symbol in enumerate(symbols):
            self.__dict__[symbol] = i
            self.lookup[i] = symbol

    def at(self, index):
        return self.lookup[index]

class Token:
    def __init__(self, tok, value, lineno, colno):
        self.tok = tok
        self.value = value
        self.lineno = lineno
        self.colno = colno

    def __str__(self):
        return f"{self.tok}({self.value})"

    def __repr__(self):
        return self.__str__()

    def cmp(self, token):
        return self.tok == token

class Lexer:
    def __init__(self, definitions: OrderedDict):
        self.current_file: str = ""
        self.text: str = ""
        self.definitions: OrderedDict = definitions
        self.tokens: List[Token] = []

    def read(self, text: str, isfile=False):
        if isfile:
            with open(text, 'r') as input_file:
                self.text = input_file.read()
                self.current_file = copy.deepcopy(text)
        else:
            self.text = text
        return self

    def lex(self):
        lineno = 0
        colno  = 0
        text = copy.deepcopy(self.text)

        count_newlines = lambda txt: txt.count('\n')
        indexof_last_newline = lambda txt: len(txt) - txt.rfind('\n')

        while text:
            matched = False
            for tok, reg in self.definitions.items():
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
                    #lineno += text[start:end].count('\n')
                    lineno += count_newlines(text[start:end])
                    #colno = len(text[start:end]) - text[start:end].rfind('\n')
                    colno = indexof_last_newline(text[start:end])
                else:
                    colno += end
                # record token
                self.tokens.append(Token(tok, text[start:end], lineno, colno))
                text = text[end:]
                break
            # ensure no infinite loop
            if not matched:
                print(f"{self.current_file}:{lineno}:{colno}\nUnexpected token(s): '{text}'")
                exit(-1)
        return self

    def strip(self, token: Syms):
        self.tokens = list(filter(lambda t: t.tok != token, self.tokens))
        return self

    def find(self, pattern: List[Syms]) -> int:
        for i, _ in enumerate(self.tokens):
            tokens = [t.tok for t in self.tokens]
            if tokens[i:i+len(pattern)] == pattern:
                return i
