import re
from grammar import *

class Token:
    def __init__(self, tok, value):
        self.tok = tok
        self.value = value
    def __str__(self):
        return f"{self.tok}({self.value})"
    def __repr__(self):
        return self.__str__()

def lex(text:str) -> list:
    tokenized = []

    while text:
        matched = False
        for tok, reg in Tokens.items():
            # look for the token with the next highest priority
            found = re.search(reg, text)
            if not found: continue
            # start / end indices of token
            start, end = found.span()
            if start != 0: continue
            matched = True
            # record token
            tokenized.append(Token(tok, text[start:end]))
            text = text[end:]
            break
        # ensure no infinite loop
        if not matched:
            print(f"Failure to tokenize:\n{text}")
            exit(-1)
    return tokenized

if __name__ == '__main__':
    a = "  12 the"
    print(lex(a))
