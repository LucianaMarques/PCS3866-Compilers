#ifndef ASCIICHARACTER_H
#define ASCIICHARACTER_H

#include <iostream>
using namespace std;

#include <string>

class asciicharacter{
public:
    asciicharacter(char ch);
    char c;
    string utility;
    string type;
    void categorize(void);
};

#endif