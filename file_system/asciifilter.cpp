#include "asciifilter.h"
#include "token.h"
#include "asciicharacter.h"

asciifilter::asciifilter(string l)
{
    this->line = l;
}

void asciifilter::extract_ascii(vector<char>& v)
{
    for (int i = 0; i < this->line.size(); i++)
    {
        cout << this->line[i] << endl;
        v.push_back(this->line[i]);
    }
}

asciicharacter * asciifilter::classify_char(char c)
{
    asciicharacter * ch = new asciicharacter(c);
    ch->categorize();
    return ch;
}