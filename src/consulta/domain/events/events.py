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

    def to_json(self):
        return {
            'consulta_id': self.consulta_id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'horario': self.horario
        }