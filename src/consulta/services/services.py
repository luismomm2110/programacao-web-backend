from uuid import uuid4

from consulta.domain.models.model import Consulta


def marcar_consulta(repositories, dados, session):
    paciente_id = dados['paciente_id']
    medico_id = dados['medico_id']
    horario = dados['horario']
    consulta = Consulta(int(uuid4()), medico_id, paciente_id, horario)
    repositories[2].add(consulta)
    session.commit()
    return 'Consulta marcada com sucesso'