#include <sstream>
#include <iostream>
#include <fstream>
#include "lexer.hpp"

Token::Token(int tok, std::string value)
    : tok{tok}, value{value}
{}

std::string Token::str()
{
    return std::to_string(tok) + "(" + value + ")";
}


Lexer::Lexer(std::vector<std::regex> definitions)
    : text{}, definitions{definitions}, tokens{}
{}

void Lexer::read(std::string input, bool isfile)
{
    if (!isfile)
        text = input;
    else {
        std::ifstream file(input);
        if (!file.is_open()) {
            std::cerr << "File " << input << " not found." << std::endl;
            std::exit(-1);
        }
        std::stringstream sstr;
        sstr << file.rdbuf();
        text = sstr.str();
    }
}

void Lexer::lex()
{
    int lineno = 0;
    int colno  = 0;
    std::string lextext = text;

    while (lextext.size() > 0) {
        bool matched = false;

        // look for the token with the next highest priority
        for (int i = 0; i < definitions.size(); i++) {
            std::smatch smatch;
            bool found = std::regex_search(lextext, smatch, definitions[i]);

            if (!found)
                continue;
            if (lextext.find(smatch[0].str()) != 0)
                continue;
            
            // regex was the next item (next starts at 0), so match
            matched = true;
            std::string match = smatch[0].str();

            if (match.find('\n') != std::string::npos) {
                lineno += std::count(match.begin(), match.end(), '\n');
                colno = match.size() - match.rfind('\n');
            }
            else {
                colno += match.size();
            }

            // record token
            tokens.push_back(Token{i, match});
            lextext = lextext.substr(match.size());

            // look for next token, start at highest priority token again
            break;
        }
        if (!matched) {
            std::cerr << "Unexpected token on line " << lineno << ":" << colno << std::endl;
            std::exit(-1);
        }
    }
}

void Lexer::strip(int tok)
{
    for (int i = 0; i < tokens.size(); i++) {
        if (tokens[i].tok == tok)
            tokens.erase(tokens.begin() + i);
    }
}
