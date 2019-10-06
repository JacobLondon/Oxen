#include <iostream>
#include "lexer.hpp"

int main()
{
    std::vector<std::regex> defs {
        std::regex{"[\\s\t\r\n]"},              // whitespace
        std::regex{"[a-zA-Z_]+[a-zA-Z0-9_]*"},  // identifier
        std::regex{"[0-9]+\\.[0-9]*"},          // float
        std::regex{"[0-9]"},                    // integer
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
    mylexer.read("10 * 5 is 50.", false);
    mylexer.lex();

    std::printf("[");
    for (Token t : mylexer.tokens) {
        std::cout << t.str(lookup) << " ";
    }
    std::printf("]\n");

    return 0;
}