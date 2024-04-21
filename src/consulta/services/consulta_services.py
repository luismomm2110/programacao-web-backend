from consulta.domain.models.model import Consulta
from consulta.services.medicos_services import tem_horario_disponivel
from consulta.services.unit_of_work import AbstractUnitOfWork


def marcar_consulta(dados, uow: AbstractUnitOfWork):
    with uow:
        medico = uow.medicos.get(dados['medico_id'])
        paciente = uow.pacientes.get_by_email(dados['email'])
        if not paciente:
            return None, 'Paciente não encontrado'
        if not medico:
            return None, 'Médico não encontrado'
        if not tem_horario_disponivel(medico.id, dados['horario'], uow):
            return None, 'Horário indisponível'
        uow.consultas.add(Consulta(
            medico_id=medico.id,
            paciente_id=paciente.id,
            horario=dados['horario']
        ))

        uow.commit()

        return 'Consulta marcada com sucesso', None


