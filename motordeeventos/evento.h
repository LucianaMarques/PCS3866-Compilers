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
		char id;
		string name;
		(*tarefa)(void);
		evento(evento * prox, int inst, char i, string n, tarefa(void));
};

#endif



