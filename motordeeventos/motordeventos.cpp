/************************

Motor de Eventos Generico

*************************/

#include "evento.h"

#include <iostream>
using namespace std;

//lista-ligada de eventos

Evento * init = new Evento(NULL, 0, '1', "init process", init_process);
Evento * current_file = new Evento(NULL, 0, '2', "current file", curr_proc);
Evento * open = new Evento(NULL, 0, '3', "open file", open_file);
Evento * close = new Evento(NULL, 0, '4', "close file", close_file);
Evento * line = new Evento(NULL, 0, '5', "position in line", position_line);
Evento * next_line = new Evento(NULL, 0, '6', "position next line", next_line);
Evento * read = new Evento(NULL, 0, '7', "read line", read_line);
Evento * end = new Evento(NULL, 0, '6', "end of process", end_process);

//mapeamento de tarefas

//declaracao de tarefas

void init_process(void);
void curr_proc(void);
void open_file(void);
void close_file(void);
void position_line(void);
void next_line(void);
void read_line(void);
void end_process(void);

int main()
{

	return 0;
}

//definicao de tarefas
