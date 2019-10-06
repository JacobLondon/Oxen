#include <iostream>
#include "lexer.hpp"

int main()
{
    enum Tokens {
        WHITESPACE,
        IDENTIFIER,
        FLOAT,
        INTEGER,
        MULTIPLY,
        ADD,
        UNKNOWN,
    };

    std::vector<std::regex> defs {
        std::regex{"[\\s\t\r\n]+"},             // whitespace
        std::regex{"[a-zA-Z_]+[a-zA-Z0-9_]*"},  // identifier
        std::regex{"[0-9]+\\.[0-9]*"},          // float
        std::regex{"[0-9]+"},                   // integer
        std::regex{"\\*"},                      // multiply
        std::regex{"\\+"},                      // add
        std::regex{"."},                        // unknown
    };

    std::vector<std::string> lookup {
        "Whitespace",
        "Identifier",
        "Float",
        "Integer",
        "Multiply",
        "Add",
        "Unknown",
    };

    Lexer mylexer{defs};
    mylexer.read("test.txt", true);
    mylexer.lex();
    mylexer.strip(WHITESPACE); // whitespace

    std::cout << "[";
    for (Token t : mylexer.tokens)
        std::cout << lookup[t.tok] << "(" << t.value << ") ";
    std::cout << "]" << std::endl;

    return 0;
}
