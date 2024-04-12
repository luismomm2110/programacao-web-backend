from consulta.domain.models.model import Consulta, agendar_consulta
from consulta.services.medicos_services import tem_horario_disponivel
from consulta.services.unit_of_work import AbstractUnitOfWork


def marcar_consulta(dados, uow: AbstractUnitOfWork):
    with uow:
        consulta_repository = uow.consultas
        medico_repository = uow.medicos
        medico = medico_repository.get(dados['medico_id'])
        if not medico:
            return 'Médico não encontrado'
        if not tem_horario_disponivel(consulta_repository, medico.id, dados['horario']):
            return 'Horário indisponível'
        medico_repository.update(medico)
        consulta_repository.add(Consulta(
            medico_id=medico.id,
            paciente_id=dados['paciente_id'],
            horario=dados['horario']
        ))

        uow.commit()

        return 'Consulta marcada com sucesso'


