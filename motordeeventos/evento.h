#include <iostream>
using namespace std;


//public types

typedef struct
{
	evento * proximo;
	int instante_programado;
	char id;
	(*tarefa)(void);
} evento;



