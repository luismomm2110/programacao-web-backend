from dataclasses import dataclass
from datetime import date
from uuid import uuid4


class Paciente:
    def __init__(self, nome: str, cpf: str):
        self.id = uuid4()
        self.nome = nome
        self.cpf = cpf

    def __repr__(self):
        return f'Paciente({self.nome}, {self.cpf})'

    def __eq__(self, other):
        if not isinstance(other, Paciente):
            return False
        return self.cpf == other.cpf

    def __hash__(self):
        return hash(self.cpf)


class Medico:
    def __init__(self, nome: str, crm: str):
        self.id = uuid4()
        self.nome = nome
        self.crm = crm
        self.agenda: dict = {}

    def agendar_consulta(self, paciente: Paciente, horario: date):
        self.agenda[horario] = paciente

    def pode_agendar_consulta(self, horario: date):
        return horario not in self.agenda

    def cancelar_consulta(self, consulta: date):
        del self.agenda[consulta]

    def __repr__(self):
        return f'Medico({self.nome}, {self.crm})'

    def __eq__(self, other):
        if not isinstance(other, Medico):
            return False
        return self.crm == other.crm

    def __hash__(self):
        return hash(self.crm)


def agendar_consulta(medico: Medico, paciente: Paciente, horario: date):
    if not medico.pode_agendar_consulta(horario):
        return 'Horário indisponível'
    medico.agendar_consulta(paciente, horario)


@dataclass(unsafe_hash=True)
class Consulta:
    id: int
    medico_id: int
    paciente_id: int
    horario: date
