#ifndef EVENTO_H
#define EVENTO_H

#include <iostream>
using namespace std;

#include <string>

//public types

class evento
{
	public:
		evento * proximo;
		int instante_programado;
		string name;
		evento(string n);
};

#endif



