from dataclasses import dataclass
from datetime import date


class Paciente:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf


class Medico:
    def __init__(self, nome: str, crm: str):
        self.nome = nome
        self.crm = crm
        self.agenda: dict = {}

    def agendar_consulta(self, paciente: Paciente, horario: date):
        self.agenda[horario] = paciente

    def pode_agendar_consulta(self, horario: date):
        return horario not in self.agenda

    def cancelar_consulta(self, consulta: date):
        del self.agenda[consulta]


def agendar_consulta(medico: Medico, paciente: Paciente, horario: date):
    if not medico.pode_agendar_consulta(horario):
        return 'Horário indisponível'
    medico.agendar_consulta(paciente, horario)