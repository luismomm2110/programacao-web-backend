import pytest

from consulta.domain.models.model import Paciente, Medico, Consulta
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
    paciente_repository.create(paciente)
    medico_repository.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario}

    resultado = services.marcar_consulta(repositories, dados, FakeSession())

    assert resultado == 'Consulta marcada com sucesso'
    assert consulta_repository.consultas[0].paciente_id == paciente.id
    assert consulta_repository.consultas[0].medico_id == medico.id
    assert consulta_repository.consultas[0].horario == horario
    assert len(consulta_repository.consultas) == 1
    assert medico_repository.medicos[0].agenda[horario] == Consulta(medico.id, paciente.id, horario)


def test_deve_retornar_horario_indisponivel():
    paciente = Paciente('Fulano', '123.456.789-00')
    medico = Medico('Dr. House', '1234')
    paciente_repository = FakePacienteRepository()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    repositories = [paciente_repository, medico_repository, consulta_repository]
    paciente_repository.create(paciente)
    medico_repository.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario}
    services.marcar_consulta(repositories, dados, FakeSession())

    outro_paciente = Paciente('Sicrano', '987.654.321-00')
    dados = {'paciente_id': outro_paciente.id, 'medico_id': medico.id, 'horario': horario}
    resultado = services.marcar_consulta(repositories, dados, FakeSession())

    assert resultado == 'Horário indisponível'
    assert len(consulta_repository.consultas) == 1

def test_deve_retornar_medico_nao_encontrado():
    paciente = Paciente('Fulano', '123.456.789-00')
    paciente_repository = FakePacienteRepository()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    repositories = [paciente_repository, medico_repository, consulta_repository]
    paciente_repository.create(paciente)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': '123', 'horario': horario}

    resultado = services.marcar_consulta(repositories, dados, FakeSession())

    assert resultado == 'Médico não encontrado'
    assert len(consulta_repository.consultas) == 0

class FakeSession():
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True