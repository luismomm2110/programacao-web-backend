from abc import abstractmethod, ABC

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.auth_repository import AbstractAuthUserRepository, SqlAlchemyAuthUserRepository, FakeAuthUserRepository
from consulta.repositories.consulta_repository import AbstractConsultaRepository, SqlAlchemyConsultaRepository, FakeConsultaRepository
from consulta.repositories.medico_repository import AbstractMedicoRepository, SqlAlchemyMedicoRepository, FakeMedicoRepository
from consulta.repositories.paciente_repository import AbstractPacienteRepository, SqlAlchemyPacienteRepository, FakePacienteRepository


class AbstractUnitOfWork(ABC):
    consultas: AbstractConsultaRepository
    medicos: AbstractMedicoRepository
    pacientes: AbstractPacienteRepository
    auth_user: AbstractAuthUserRepository

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit (self):
        raise NotImplementedError

    @abstractmethod
    def rollback (self):
        raise NotImplementedError


engine = create_engine('postgresql://user:password@localhost:5432/consultas')
DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = DEFAULT_SESSION_FACTORY()
        self.consultas = SqlAlchemyConsultaRepository(self.session)
        self.medicos = SqlAlchemyMedicoRepository(self.session)
        self.pacientes = SqlAlchemyPacienteRepository(self.session)
        self.auth_user = SqlAlchemyAuthUserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.consultas = FakeConsultaRepository()
        self.medicos = FakeMedicoRepository()
        self.pacientes = FakePacienteRepository()
        self.auth_user = FakeAuthUserRepository()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass