from dataclasses import dataclass
from datetime import date

class Event:
    pass

@dataclass
class ConsultaCriada(Event):
    consulta_id: int
    paciente_nome: str
    medico_nome: str
    paciente_id: int
    medico_id: int
    horario: date

    def to_json(self):
        return {
            'consulta_id': self.consulta_id,
            'paciente_nome': self.paciente_nome,
            'medico_nome': self.medico_nome,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'horario': self.horario,
            "consulta_cancelada": False
        }


@dataclass
class ConsultaCancelada(Event):
    consulta_id: int

    def to_json(self):
        return {
            "consulta_cancelada": True,
            "consulta_id": self.consulta_id
        }
