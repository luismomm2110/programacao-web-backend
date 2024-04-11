from consulta.domain.models.model import Paciente, Medico
from consulta.repositories.consulta_repository import FakeConsultaRepository
from consulta.repositories.medico_repository import FakeMedicoRepository
from consulta.services.consulta_services import marcar_consulta
from consulta.services.medicos_services import tem_horario_disponivel


def test_pode_marcar_consulta_quando_tem_horario_disponivel():
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    medico = _criar_medico()
    paciente = _criar_paciente()
    medico_repository.add(medico)
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': '2022-01-01'}
    marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    resultado = tem_horario_disponivel(consulta_repository, medico.id, '2022-02-01')

    assert resultado is True


def test_nao_pode_marcar_consulta_quando_nao_tem_horario_disponivel():
    medico_repository = FakeMedicoRepository()
    consulta_repository = FakeConsultaRepository()
    medico = _criar_medico()
    paciente = _criar_paciente()
    medico_repository.add(medico)
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': '2022-01-01'}
    marcar_consulta(FakeSession(), medico_repository, consulta_repository, dados)

    resultado = tem_horario_disponivel(consulta_repository, medico.id, '2022-01-01')

    assert resultado is False

class FakeSession:
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
