#include <iostream>
#include <string>
using namespace std;

#include "filesystem.h"
#include "asciifilter.h"
#include "asciicharacter.h"
#include "evento.h"
#include "lexicanalyzer.h"
#include "token.h"

#include <queue>

// lista ligada de eventos
queue<evento *> fila_eventos;   

/* General macros */
// File System
string f = "file2.txt";
filesystem * file_system = new filesystem(f); 
ifstream file;

// ASCII Filter
asciifilter * ascii_filter = new asciifilter("\n");
vector<string> lines;

// ASCII Characters
vector<char> vec;
vector<asciicharacter *> characters;

// Tokens from pre-alaysis

vector<token *> tokens;

/**************************************/

/* Public methods */

void trata_evento(evento * e);

int main()
{
    fila_eventos.push(new evento("init process"));
    fila_eventos.push(new evento("open file"));
    fila_eventos.push(new evento("read lines"));
    fila_eventos.push(new evento("extract ascii characters"));
    fila_eventos.push(new evento("categorize ascii characters"));
    fila_eventos.push(new evento("close file"));
    while(!fila_eventos.empty())
    {
        cout << fila_eventos.front()->name << endl;
        trata_evento(fila_eventos.front());
        fila_eventos.pop();
    }
    cout << vec.size();
}

void trata_evento(evento * e)
{
    if (e->name == "init process")
    {
        cout << "Init compiler" << endl;
    }
    else if (e->name == "open file")
    {
        file_system->open_file(file);        
    }
    else if (e->name == "read lines")
    {
        while(!file.eof())
        {
            string line = file_system->read_line(file);
            lines.push_back(line);
        }
    }
    else if (e->name == "extract ascii characters")
    {
        for (int i = 0; i < lines.size() - 1; i ++)
        {
            ascii_filter->line = lines[i];
            cout << lines[i] << endl;
            ascii_filter->extract_ascii(vec);
        }
    }
    else if (e->name == "categorize ascii characters")
    {
        for (int i = 0; i < vec.size(); i ++)
        {
            asciicharacter * a = ascii_filter->classify_char(vec[i]);
            //cout << a->type << " " << a->utility << endl;
            characters.push_back(a);
        }
    }
    else if (e->name == "close file")
    {
        file_system->close_file(file);
    }
}