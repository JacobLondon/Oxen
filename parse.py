from copy import copy
from lexer import *
from grammar import *

class Node:
    TITLE = "Node{"
    def __init__(self, gtok):
        self.gtok = gtok
        self.children = []
        self.action = None
    def __str__(self):
        builder = Node.TITLE
        if self.gtok:
            builder += f"{self.gtok}" + "{"
        for c in self.children:
            builder += f"{str(c)}"
        if self.gtok:
            builder += "}"
        if builder != Node.TITLE:
            builder += "}"
        else:
            builder = ""
        return builder
    def __repr__(self):
        return self.__str__()

def terminals(tokens:list, parent):
    # 1:1, for every Token, there should be a GTok
    for i, _ in enumerate(tokens):
        # is the current node a Node or Token?
        # if it's a Token, it is terminal
        if type(tokens[i]) == Token:
            # make a Node out of it
            # turn into tuple to check in Grammar
            tup = (tokens[i].tok,)
            # check if it, by itself, is a subgrammar
            for gtok, subgrammars in Grammar.items():
                if tup in subgrammars:
                    # we found a subgrammar to use for this Token
                    # make a Node out of it
                    node = Node(gtok)
                    node.children = [tokens[i]]
                    node.action = Grammar[gtok][tup]
                    # insert the nodified Token into the root Node
                    parent.children.append(node)
            pass # finished this item, skip the non-terminals

def nonterminals(parent):
    i = -1
    while True:
        if i + 1 < len(parent.children): i += 1
        else: break
    
        for gtok, subgrammars in Grammar.items():
            for subgtok, action in subgrammars.items():
                # get the subgrammar tuple (1-any length), and check if those items which belong to
                # parent's children at the current slice is the same
                length = len(subgtok)
                # check if the current token is a subgrammar
                tup = tuple([c.gtok for c in parent.children[i:i+length]])
                #print(i, length, gtok, tup, parent.children[i])

                # Note: the slice may no longer be the same length if OOB
                if len(tup) != length:
                    continue

                # same args, so check if it is a match
                if tup == subgtok:
                    # we found a subgrammar for this GTok, make a Node for it
                    node = Node(gtok)
                    # there are 'length' number of children in this Node
                    # add them to the current node
                    node.children = copy(parent.children[i:i+length])
                    node.action = action # Grammar[gtok][tup] <- probably less readable
                    # now there are 'length' number of unecessary children in parent
                    # remove the slice of children, and replace with 'node'
                    remove_at = list(range(i, i+length))
                    # delete the old values
                    parent.children = [val for j, val in enumerate(parent.children) if j not in remove_at]
                    # insert the new value
                    parent.children.insert(i, node)
                    # correct for shortened i
                    i -= len(remove_at) + 1
                    break
            # end for
        # end for
    # end while

def evaluate(root):
    for child in root.children:
        # terminal GTok holding the Token singleton
        if type(child) == Node and len(child.children) == 1 and type(child.children[0]) == Token:
            return child.action(child.children[0].value)
        # non-terminal GTok
        if type(child) != Token:
            return child.action(*[evaluate(c) for c in child.children])
        if type(child) == Token:
            return child.value
        
if __name__ == '__main__':
    while True:
        root = Node(None)
        tokens = strip(lex(input(">>> ")))
        terminals(tokens, root)
        nonterminals(root)
        print(evaluate(root))
        with open('temp.c', 'w') as temp:
            temp.write(str(root))
