import random

from auth.model import AuthUser
from consulta.domain.models.model import Paciente
from consulta.services.unit_of_work import AbstractUnitOfWork


def criar_conta_paciente(dados, uow: AbstractUnitOfWork):
    with uow:
        paciente_repository = uow.pacientes
        auth_repository = uow.auth_user
        if paciente_repository.get_by_email(dados['email']):
            raise ValueError('Paciente já cadastrado')
        paciente = Paciente(
            paciente_id=random.randint(1, 100000),
            email=dados['email'],
            nome=dados['nome'],
            cpf=dados['cpf']
        )
        paciente_repository.create(paciente)
        usuario = AuthUser(
            user_id=random.randint(1, 100000),
            username=dados['nome'],
            email=dados['email'],
            password=dados['password'],
            entity_id=paciente.id,
        )
        auth_repository.add(usuario)
        uow.commit()
        return paciente
