import random

from auth.model import AuthUser
from consulta.domain.models.model import Consulta, agendar_consulta, Paciente


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


def criar_conta_paciente(repositories, dados, session):
    paciente = Paciente(
        paciente_id=random.randint(1, 100000),
        nome=dados['nome'],
        cpf=dados['cpf']
    )
    repositories[1].create(paciente)
    usuario = AuthUser(
        user_id=random.randint(1, 100000),
        username=dados['nome'],
        password=dados['password'],
        entity_id=paciente.id,
    )
    repositories[0].add(usuario)
    session.commit()
    return paciente
