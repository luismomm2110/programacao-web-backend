from uuid import uuid4

from consulta.domain.models.model import Consulta, agendar_consulta


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
    