from consulta.domain.models.model import Consulta, agendar_consulta
from consulta.services.medicos_services import tem_horario_disponivel
from consulta.services.unit_of_work import AbstractUnitOfWork


def marcar_consulta(dados, uow: AbstractUnitOfWork):
    with uow:
        medico = uow.medicos.get(dados['medico_id'])
        if not medico:
            return 'Médico não encontrado'
        if not tem_horario_disponivel(medico.id, dados['horario'], uow):
            return 'Horário indisponível'
        uow.medicos.update(medico)
        uow.consultas.add(Consulta(
            medico_id=medico.id,
            paciente_id=dados['paciente_id'],
            horario=dados['horario']
        ))

        uow.commit()

        return 'Consulta marcada com sucesso'


