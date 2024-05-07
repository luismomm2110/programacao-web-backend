from dataclasses import dataclass
from datetime import date

class Event:
    pass

@dataclass
class ConsultaCriada(Event):
    consulta_id: int
    paciente_id: int
    medico_id: int
    horario: date