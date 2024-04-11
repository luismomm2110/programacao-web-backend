import pytest

from consulta.repositories.medico_repository import FakeMedicoRepository
from consulta.services.medicos_services import criar_medico


def test_cria_medico():
    session = FakeSession()
    repo = FakeMedicoRepository()

    criar_medico(session, repo, 'Dr. House', '1234')

    assert repo.medicos[0].nome == 'Dr. House'
    assert repo.medicos[0].crm == '1234'


class FakeSession:
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True
