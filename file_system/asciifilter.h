#ifndef ASCIIFILTER_H
#define ASCIIFILTER_H

#include <iostream>
using namespace std;

#include "token.h"
#include "asciicharacter.h"

#include <string>
#include <vector>

class asciifilter{
public:
    asciifilter(string l);
    string line;
    vector<char> chars;
    void extract_ascii(vector<char>& v);
    asciicharacter * classify_char(char c);
};

#endif