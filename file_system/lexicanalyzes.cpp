#include "lexicanalyzer.h"

lexicanalyzer::lexicanalyzer(void)
{

}

void lexicanalyzer::pre_analysis(vector<token *>& tokens, vector<asciicharacter *> characters)
{
    int i = 0;
    string key;
    while (i < characters.size())
    {

        i++;
    }
}

node_t * lexicanalyzer::next_node(node_t current_node, string next_char_type)
{
    node_t digit; 
    digit->type = "digit";
    if (current_node->type_node == "digit")
    {
        if (next_char_type == "digit")
        {
            current_node = digit;
        }
        else if (next_char_type == "delimiter")
        {
            
        }
    }
}