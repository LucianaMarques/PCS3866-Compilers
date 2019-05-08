from MotorDeEventos import MotorDeEventos, Evento

m = MotorDeEventos()

arquivo = "input3.toy"
m.add_event(Evento("extrair_linhas", arquivo))

m.event_cycle()