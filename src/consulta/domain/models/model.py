from dataclasses import dataclass
from datetime import date
from random import random
from uuid import uuid4


class Paciente:
    def __init__(self, paciente_id: int, nome: str, email: str, cpf: str):
        self.id = paciente_id
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return f'Paciente({self.nome}, {self.cpf})'

    def __eq__(self, other):
        if not isinstance(other, Paciente):
            return False
        return self.cpf == other.cpf

    def __hash__(self):
        return hash(self.cpf)

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf
        }

class Medico:
    def __init__(self, medico_id: int, nome: str, crm: str):
        self.id = medico_id
        self.nome = nome
        self.crm = crm
        self.agenda: dict = {}

    def pode_agendar_consulta(self, horario: date):
        return horario not in {consulta.horario for consulta in self.agenda.values()}

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

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'crm': self.crm
        }


def agendar_consulta(medico: Medico, paciente_id: int, horario: date):
    if not medico.pode_agendar_consulta(horario):
        return 'Horário indisponível'


@dataclass(unsafe_hash=True)
class Consulta:
    medico_id: int
    paciente_id: int
    horario: date

    def __eq__(self, other):
        if not isinstance(other, Consulta):
            return False
        return self.medico_id == other.medico_id and self.paciente_id == other.paciente_id and self.horario == other.horario
    
    def to_json(self):
        return {
            'id': self.id,
            'medico_id': self.medico_id,
            'paciente_id': self.paciente_id,
            'horario': self.horario.isoformat()
        }