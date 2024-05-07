from domain.events.events import ConsultaCriada, Event


def handle(event: Event):
    for handler in HANDLERS(type(event)):
        handler(event)


HANDLERS = {ConsultaCriada: [notificar_medico]}