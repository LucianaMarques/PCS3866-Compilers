#ifndef LEXICANALYZER_H
#define LEXICANALYZER_H

#include <iostream>
using namespace std;

#include "token.h"
#include "asciicharacter.h"

#include <string>

typedef struct node{
    string type_node;
} node_t;

class lexicanalyzer{
public:
    lexicanalyzer();
    void pre_analysis(vector<token *>& tokens);
    node_t next_node(node_t current_node, string next_char_type);
};

#endif