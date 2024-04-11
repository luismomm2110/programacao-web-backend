import pytest

from consulta.domain.models.model import Paciente, Medico, Consulta
from consulta.repositories.consulta_repository import FakeConsultaRepository
from consulta.repositories.medico_repository import FakeMedicoRepository
from consulta.repositories.paciente_repository import FakePacienteRepository
from consulta.services.consulta_services import marcar_consulta


def test_marca_consulta():
    paciente, medico = _criar_paciente(), _criar_medico()
    paciente_repository = FakePacienteRepository()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    paciente_repository.create(paciente)
    medico_repository.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario}

    resultado = marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    assert resultado == 'Consulta marcada com sucesso'
    assert consulta_repository.consultas[0].paciente_id == paciente.id
    assert consulta_repository.consultas[0].medico_id == medico.id
    assert consulta_repository.consultas[0].horario == horario
    assert len(consulta_repository.consultas) == 1


def test_deve_retornar_horario_indisponivel():
    paciente, medico = _criar_paciente(), _criar_medico()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    medico_repository.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario}
    marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    outro_paciente = _criar_paciente(paciente_id=2, nome='Maria', cpf='123.456.789-00')
    dados = {'paciente_id': outro_paciente.id, 'medico_id': medico.id, 'horario': horario}
    resultado = marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    assert resultado == 'Horário indisponível'
    assert len(consulta_repository.consultas) == 1


def test_deve_retornar_medico_nao_encontrado():
    paciente = _criar_paciente()
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': '123', 'horario': horario}

    resultado = marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    assert resultado == 'Médico não encontrado'
    assert len(consulta_repository.consultas) == 0


class FakeSession():
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True


def _criar_paciente(**kwargs):
    default = {'paciente_id': 1, 'nome': 'Fulano', 'cpf': '123.456.789-00', 'email': 'luis@gmail.com'}
    paciente = Paciente(**{**default, **kwargs})

    return paciente


def _criar_medico():
    medico = Medico(1, 'Dr. House', '1234')

    return medico
