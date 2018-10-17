/************************

Motor de Eventos Generico

*************************/

#include "evento.h"

#include <iostream>
using namespace std;
#include "map"

//declaracao de eventos de interesse

Evento * init = new Evento(NULL, 0, '1', "init process", init_process);
Evento * current_file = new Evento(NULL, 0, '2', "current file", curr_proc);
Evento * open = new Evento(NULL, 0, '3', "open file", open_file);
Evento * close = new Evento(NULL, 0, '4', "close file", close_file);
Evento * line = new Evento(NULL, 0, '5', "position in line", position_line);
Evento * next_line = new Evento(NULL, 0, '6', "position next line", next_line);
Evento * read = new Evento(NULL, 0, '7', "read line", read_line);
Evento * end = new Evento(NULL, 0, '6', "end of process", end_process);

//lista ligada

Evento * head = new Evento(NULL, 0, '0', "head of linked list", linked_list);

//mapeamento de tarefas

unordered_map <char, (*tarefa)(void)> events_map;
events_map.insert(pair<char, (*tarefa)(void)> ('1', init_process));
events_map.insert(pair<char, (*tarefa)(void)> ('2', curr_proc));
events_map.insert(pair<char, (*tarefa)(void)> ('3', open_file));
events_map.insert(pair<char, (*tarefa)(void)> ('4', close_file));
events_map.insert(pair<char, (*tarefa)(void)> ('5', position_line));
events_map.insert(pair<char, (*tarefa)(void)> ('6', next_line));
events_map.insert(pair<char, (*tarefa)(void)> ('7', read_line));
events_map.insert(pair<char, (*tarefa)(void)> ('8', end_process));                                                                                                                                      

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
