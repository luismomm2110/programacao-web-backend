from datetime import datetime, date

import pytest

from consulta.domain.models.model import Paciente, Medico, Consulta
from consulta.repositories.consulta_repository import FakeConsultaRepository
from consulta.repositories.medico_repository import FakeMedicoRepository
from consulta.services.consulta_services import marcar_consulta
from consulta.services.unit_of_work import FakeUnitOfWork


def test_marca_consulta():
    uow = FakeUnitOfWork()
    paciente, medico = _criar_paciente(), _criar_medico()
    uow.pacientes.create(paciente)
    uow.medicos.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario, 'email': paciente.email}

    resultado, erro = marcar_consulta(dados, uow)

    assert resultado == 'Consulta marcada com sucesso'
    assert erro is None
    consulta = uow.consultas.get_by_paciente_id(paciente.id)[0]
    assert date(2022, 1, 1) == consulta.horario
    assert consulta.medico_id == medico.id
    assert consulta.paciente_id == paciente.id


def test_deve_retornar_horario_indisponivel():
    uow = FakeUnitOfWork()
    paciente, medico = _criar_paciente(), _criar_medico()
    uow.pacientes.create(paciente)
    uow.medicos.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario, 'email': paciente.email}
    marcar_consulta(dados, uow)

    outro_paciente = _criar_paciente(paciente_id=2, nome='Maria', cpf='123.456.789-00')
    dados = {'paciente_id': outro_paciente.id, 'medico_id': medico.id, 'horario': horario, 'email': outro_paciente.email}
    _, erro = marcar_consulta(dados, uow)

    assert erro == 'Horário indisponível'
    assert len(uow.consultas.get_all()) == 1


def test_deve_retornar_medico_nao_encontrado():
    uow = FakeUnitOfWork()
    paciente = _criar_paciente()
    uow.pacientes.create(paciente)
    horario = '2022-01-01'
    dados = {'paciente_id': paciente.id, 'medico_id': '123', 'horario': horario, 'email': paciente.email}

    _, erro = marcar_consulta(dados, uow)

    assert erro == 'Médico não encontrado'
    assert len(uow.consultas.get_all()) == 0

def test_deve_retornar_paciente_nao_encontrado():
    uow = FakeUnitOfWork()
    medico = _criar_medico()
    uow.medicos.add(medico)
    horario = '2022-01-01'
    dados = {'paciente_id': '123', 'medico_id': medico.id, 'horario': horario, 'email': 'foobar'}

    _, erro = marcar_consulta(dados, uow)

    assert erro == 'Paciente não encontrado'


def test_deve_retornar_erro_quando_data_invalida():
    uow = FakeUnitOfWork()
    paciente, medico = _criar_paciente(), _criar_medico()
    uow.pacientes.create(paciente)
    uow.medicos.add(medico)
    horario = 'foo'
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': horario, 'email': paciente.email}
    with pytest.raises(ValueError) as excinfo:
        marcar_consulta(dados, uow)

    assert str(excinfo.value) == 'Formato de data inválido. Use o formato YYYY-MM-DD'


def _criar_paciente(**kwargs):
    default = {'paciente_id': 1, 'nome': 'Fulano', 'cpf': '123.456.789-00', 'email': 'luis@gmail.com'}
    paciente = Paciente(**{**default, **kwargs})

    return paciente


def _criar_medico():
    medico = Medico(1, 'Dr. House', '1234')

    return medico
