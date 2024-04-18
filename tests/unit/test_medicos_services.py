from consulta.domain.models.model import Paciente, Medico
from consulta.services.consulta_services import marcar_consulta
from consulta.services.medicos_services import tem_horario_disponivel, criar_medico
from consulta.services.unit_of_work import FakeUnitOfWork


def test_pode_marcar_consulta_quando_tem_horario_disponivel():
    uow = FakeUnitOfWork()
    medico = _criar_medico()
    paciente = _criar_paciente()
    criar_medico(medico.nome, medico.crm, uow)
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': '2022-01-01', 'email': paciente.email}
    marcar_consulta(dados, uow)

    resultado = tem_horario_disponivel(medico.id, '2022-02-01', uow)

    assert resultado is True


def test_nao_pode_marcar_consulta_quando_nao_tem_horario_disponivel():
    uow = FakeUnitOfWork()
    medico = _criar_medico()
    uow.medicos.add(medico)
    paciente = _criar_paciente()
    uow.pacientes.create(paciente)
    dados = {'paciente_id': paciente.id, 'medico_id': medico.id, 'horario': '2022-01-01', 'email': paciente.email}
    marcar_consulta(dados, uow)

    resultado = tem_horario_disponivel(medico.id, '2022-01-01', uow)

    assert resultado is False


def test_cria_medico():
    uow = FakeUnitOfWork()

    criar_medico('Dr. House', '1234', uow)

    assert len(uow.medicos.get_all()) == 1
    medico = uow.medicos.get_all()[0]
    assert medico.nome == 'Dr. House'


def _criar_paciente(**kwargs):
    default = {'paciente_id': 1, 'nome': 'Fulano', 'cpf': '123.456.789-00', 'email': 'luis@gmail.com'}
    paciente = Paciente(**{**default, **kwargs})

    return paciente


def _criar_medico():
    medico = Medico(1, 'Dr. House', '1234')

    return medico
