#include <string>
#include <regex>
#include <unordered_map>
#include <vector>

struct Token {
    Token(int tok, std::string value);
    std::string str(std::vector<std::string> lookup);
    int tok;
    std::string value;
};

struct Lexer {
    Lexer(std::vector<std::regex> definitions);
    void read(std::string input, bool isfile);
    void lex();
    void strip(int tok);

    std::string text;
    std::vector<std::regex> definitions;
    std::vector<Token> tokens;
};
