import random

from auth.auth_repository import SqlAlchemyAuthUserRepository
from auth.model import AuthUser
from consulta.domain.models.model import Consulta, agendar_consulta, Paciente
from consulta.repositories.paciente_repository import SqlAlchemyPacienteRepository


def marcar_consulta(repositories, dados, session):
    medico = repositories[1].get(dados['medico_id'])
    if not medico:
        return 'Médico não encontrado'
    resultado = agendar_consulta(medico, dados['paciente_id'], dados['horario'])
    if resultado == 'Horário indisponível':
        return resultado
    repositories[1].update(medico)
    repositories[2].add(Consulta(
        medico_id=medico.id,
        paciente_id=dados['paciente_id'],
        horario=dados['horario']
    ))

    session.commit()

    return 'Consulta marcada com sucesso'


def criar_conta_paciente(
        auth_repository: SqlAlchemyAuthUserRepository,
        paciente_repository: SqlAlchemyPacienteRepository,
        dados,
        session):
    if paciente_repository.get_by_email(dados['email']):
        raise ValueError('Paciente já cadastrado')
    paciente = Paciente(
        paciente_id=random.randint(1, 100000),
        email=dados['email'],
        nome=dados['nome'],
        cpf=dados['cpf']
    )
    paciente_repository.create(paciente)
    usuario = AuthUser(
        user_id=random.randint(1, 100000),
        username=dados['nome'],
        password=dados['password'],
        entity_id=paciente.id,
    )
    auth_repository.add(usuario)
    session.commit()
    return paciente
