#include "lexer.hpp"

Token::Token(int tok, std::string value)
    : tok{tok}, value{value}
{

}

std::string Token::str(std::vector<std::string> lookup)
{
    return lookup[tok] + "(" + value + ")";
}

Lexer::Lexer(std::vector<std::regex> definitions)
    : text{}, definitions{definitions}, tokens{}
{

}

void Lexer::read(std::string input, bool isfile)
{
    if (!isfile)
        text = input;
}

void Lexer::lex()
{
    int lineno = 0;
    int colno  = 0;
    std::string lextext = text;

    while (lextext.size() > 0) {
        bool matched = false;
        for (int i = 0; i < definitions.size(); i++) {
            // look for the token with the next highest priority
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
        }
    }
}

void Lexer::strip(int tok)
{
    
}
