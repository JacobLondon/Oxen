
#include <vector>
#include <iostream>
#include <string>

using std::vector;
using std::string;
using std::cerr;
using std::cout;

struct node {
    vector<int> self;
    vector<node> children;
    node *parent;

    node(vector<int> self, node *parent);
};
node::node(vector<int> self, node *parent)
: self{self}, children{}, parent(parent)
{}

vector<vector<int>> rules {
    {0, 1, 2},
    {1, 2},
    {0, 2},
    {1, 1},
};

string str(vector<int> vec)
{
    string result = "";
    for (auto ch : vec)
        result += std::to_string(ch);
    return result;
}

void parse(vector<int> d)
{
    node root(vector<int>{}, nullptr);
    vector<int> cur;
    int probe = 1;

    auto cmp = [](vector<int> vec) {
        for (int i = 0; i < vec.size(); i++)
            for (int j = 0; j < rules.size(); j++) {
                if (rules[j] == vec) return j;
            }
        return -1;
    };

    auto shift = [&probe]() {
        probe++;
    };

    auto reduce = []() {

    };

    for (int i = 0; i < d.size(); i++) {
        int rule;
        vector<int> check = vector<int>{d.begin() + i, d.begin() + probe};
        if (rule = cmp(check)) {
            if (rule == -1) cerr << "Invalid definition " << str(check) << "\n"; std::exit(-1);
            node hit = node{check, &root};
            reduce();
        } else {
            shift();
        }
    }
}
