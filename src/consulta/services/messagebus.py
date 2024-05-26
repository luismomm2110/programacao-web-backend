from consulta.domain.events import events
from consulta.domain.events.events import ConsultaCriada, Event
from consulta.services.consulta_services import handle_consulta_criada
from consulta.services.unit_of_work import AbstractUnitOfWork


def handle(event: Event, uow: AbstractUnitOfWork):
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow))
            queue.extend(uow.collect_new_events())
    return results


HANDLERS = {
    events.ConsultaCriada: [handle_consulta_criada]
}

