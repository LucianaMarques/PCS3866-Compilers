#include <iostream>
using namespace std;

#include <string>

#include "asciicharacter.h"

asciicharacter::asciicharacter(char ch)
{
    this->c = ch;
}

void asciicharacter::categorize(void)
{
    if (this->c == ' ')
    {
        this->type = "disposable";
        this->utility = "delimiter";
    }
    else if (this->c >= '0' && this->c <= '9')
    {
        this->type = "useful";
        this->utility = "number";
    }
    else if ((this->c >= 'a' && this->c <= 'z') || (this->c >= 'A' && this->c <= 'Z'))
    {
        this->type = "useful";
        this->utility = "letter";
    }
    else if ((this->c >= '!' && this->c <= '/') || (this->c >= ':' && this->c <= '@') || (this->c >= '[' && this->c <= '`') || (this->c >= '}' && this->c <= '~'))
    {
        this->type = "useful";
        this->utility = "special";
    }
}
