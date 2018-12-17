#include <iostream>
using namespace std;

#include "evento.h"

evento::evento(string n)
{
	this->name = n;
	this->proximo = NULL;
}

