from datetime import date

from consulta.domain.models.model import Consulta
from consulta.services.medicos_services import tem_horario_disponivel
from consulta.services.unit_of_work import AbstractUnitOfWork
from consulta.domain.events.events import ConsultaCriada


def marcar_consulta(dados, uow: AbstractUnitOfWork):
    with uow:
        medico = uow.medicos.get(dados['medico_id'])
        paciente = uow.pacientes.get_by_email(dados['email'])
        if not medico:
            return 'Médico não encontrado'
        if not tem_horario_disponivel(medico.id, dados['horario'], uow):
            return 'Horário indisponível'
        uow.consultas.add(Consulta(
            medico_id=medico.id,
            paciente_id=paciente.id,
            horario=dados['horario']
        ))
        medico.eventos.append(ConsultaCriada(
            consulta_id=medico.id,
            paciente_id=paciente.id,
            medico_id=medico.id,
            horario=dados['horario']
        ))


        uow.commit()

        return 'Consulta marcada com sucesso'


