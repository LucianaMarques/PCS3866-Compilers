#ifndef TOKEN_H
#define TOKEN_H

#include <iostream>
using namespace std;

#include <string>

class token{
public:
    token(string t, string k);
    string key;
    string type;
};

#endif