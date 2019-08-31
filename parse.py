from token import *
from grammar import *

class Node:
    def __init__(self, tok=None, value=None, terminal=False):
        self.tok = tok
        self.value = value
        self.parent = None
        self.children = []
        self.terminal = terminal
    def __str__(self):
        return str(self.tok) + str(self.children)
    def __repr__(self):
        return self.__str__()

root = Node()

# will just work
def parse(tokens:list):
    for i, tok in enumerate(tokens):
        for gtok, grammars in Grammar.items():
            for grammar, action in grammars.items():
                # use the first grammar encountered
                if tuple(map(lambda t: t.tok, tokens[i:i+len(grammar)])) == grammar:
                    tokens[i] = Token(gtok, tok)
                    parse(tokens)
                    break
    return tokens

def nparse(nodes:list, parent, start=0):
    print('='*10)
    iterate = iter(range(start, len(nodes)))
    for i in iterate:
        for gtok, grammars in Grammar.items():
            for grammar, action in grammars.items():
                subgrammar = tuple(map(lambda n: n.value.tok, nodes[i:i+len(grammar)]))
                if subgrammar == grammar:
                    node = Node()
                    # consume that many blank spots, leaving one spot for the replacement node
                    for j in range(len(grammar) - 1):
                        try: next(iterate)
                        except: pass
                        node.children.append(nodes[i+j])
                    if nodes[i].terminal:
                        node.tok = nodes[i].value.tok
                        node.value = nodes[i].value
                    else:
                        node.tok = gtok
                        node.value = None
                    
                    # parse children if non terminal
                    if not nodes[i].terminal:
                        nparse(node.children, node)

                    # insert replacement node
                    for j, _ in enumerate(nodes):
                        if j <= i or j >= i+len(grammar):
                            nodes[j] = nodes[j]
                        else:
                            # make the node terminal as it was already parsed
                            node.terminal = True
                            nodes[j] = node
                    
                    # reparse until all grammar has been read
                    nparse(nodes, parent, len(grammar))

                    break

def nodify(tokens:list):
    nodes = []
    for tok in tokens:
        nodes.append(Node(value=tok, terminal=True))
    return nodes


#Operation[Expression[Number[Integer(2)]], Add(), Expression[Number[Float(1.1)]]]

if __name__ == '__main__':
    tokens = strip(lex("2 + 1.1"))
    #print(nodify(tokens))
    nparse(nodify(tokens), root)
    print()
    print(root)
    """ast = parse(tokens)
    print(ast)
    for node in ast:
        if node == GTok.Operation:
            Grammar[node]
    """
