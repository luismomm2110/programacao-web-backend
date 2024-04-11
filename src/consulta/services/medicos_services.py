import random

from consulta.domain.models.model import Medico


def tem_horario_disponivel(consulta_repository, medico_id, data):
    consultas = consulta_repository.get_by_medico_id(medico_id)
    return data not in {consulta.horario for consulta in consultas}


def criar_medico(sessao, medico_repository, nome, crm):
    medico = Medico(
        medico_id=random.randint(1, 100000),
        nome=nome,
        crm=crm
    )
    medico_repository.add(medico)

    sessao.commit()

    return medico
