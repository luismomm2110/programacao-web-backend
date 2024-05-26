import random
from datetime import date, datetime

from consulta.domain.models.model import Medico
from consulta.services.unit_of_work import AbstractUnitOfWork


def tem_horario_disponivel(medico_id, data, uow):
    with uow:
        consultas = uow.consultas.get_by_medico_id(medico_id)
        return data not in {consulta.horario for consulta in consultas}


def criar_medico(nome, crm, uow: AbstractUnitOfWork):
    with uow:
        medico = Medico(
            medico_id=random.randint(1, 100000),
            nome=nome,
            crm=crm
        )
        uow.medicos.add(medico)
        uow.commit()

        return medico.to_json()
