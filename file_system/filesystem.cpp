/************************

	File System

*************************/

#include "filesystem.h"
#include <iostream>
using namespace std;
#include <string>               

filesystem::filesystem(string f)
{
    this->file = f;
}

void filesystem::open_file(ifstream& file)
{
    file.open(this->file, std::ifstream::in);
}

void filesystem::close_file(ifstream& file)
{
    file.close();
}

string filesystem::read_line(ifstream& file)
{
    string line;
    getline(file,line);
    line.erase(line.size(), 1);
    return line;
}

