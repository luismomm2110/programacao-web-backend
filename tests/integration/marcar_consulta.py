import pytest

from consulta.domain.models.model import Paciente, Medico
from consulta.repositories.consulta_repository import FakeConsultaRepository
from consulta.repositories.medico_repository import FakeMedicoRepository
from consulta.repositories.paciente_repository import FakePacienteRepository
from consulta.services import services


def test_marca_consulta():
    paciente = Paciente('Fulano', '123.456.789-00')
    medico = Medico('Dr. House', '1234')
    paciente_repository = FakePacienteRepository()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    repositories = [paciente_repository, medico_repository, consulta_repository]
    paciente_repository.create_paciente(paciente)
    medico_repository.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario}

    resultado = services.marcar_consulta(repositories, dados, FakeSession())

    assert resultado == 'Consulta marcada com sucesso'
    assert consulta_repository.consultas[0].paciente_id == paciente.id

class FakeSession():
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True
