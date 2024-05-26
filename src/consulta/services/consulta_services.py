from consulta.adapters.rabbitmq_eventpublisher import RabbitMQEventPublisher
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
        medico.events.append(ConsultaCriada(
            consulta_id=medico.id,
            paciente_id=paciente.id,
            medico_id=medico.id,
            horario=dados['horario']
        ))

        try:
            rabbitmq = RabbitMQEventPublisher('localhost')
            rabbitmq.publish(ConsultaCriada(
                consulta_id=medico.id,
                paciente_id=paciente.id,
                medico_id=medico.id,
                horario=dados['horario']
            ).to_json())
        except Exception as e:
            print(e)
            pass
        uow.commit()

        return 'Consulta marcada com sucesso'


def handle_consulta_criada(event: ConsultaCriada, uow: AbstractUnitOfWork):
    rq = RabbitMQEventPublisher('localhost')
    rq.publish(event)
