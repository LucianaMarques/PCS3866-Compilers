#ifndef FILESYSTEM_H
#define FILESYSTEM_H

#include <iostream>
using namespace std;
#include <string>
#include <fstream>


class filesystem  
{
public:
    string file;
    filesystem(string f);
    void open_file(ifstream& f);
    void close_file(ifstream& f);
    string read_line(ifstream& f);
    void end_line(void);
};



#endif