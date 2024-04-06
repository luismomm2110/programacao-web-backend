from abc import ABC, abstractmethod
from typing import List

from consulta.domain.models.model import Paciente


class AbstractPacienteRepository(ABC):
    @abstractmethod
    def get(self, paciente_id: int) -> Paciente:
        pass

    @abstractmethod
    def get_all(self) -> List[Paciente]:
        pass

    @abstractmethod
    def create(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def update(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def delete(self, paciente_id: int) -> None:
        pass


class SqlAlchemyPacienteRepository(AbstractPacienteRepository):
    def __init__(self, session):
        self.session = session

    def get(self, paciente_id: int) -> Paciente:
        return self.session.query(Paciente).filter_by(id=paciente_id).first()

    def get_by_email(self, email: str) -> Paciente:
        return self.session.query(Paciente).filter_by(email=email).first()

    def get_all(self) -> List[Paciente]:
        return self.session.query(Paciente).all()

    def create(self, paciente: Paciente) -> Paciente:
        self.session.add(paciente)
        self.session.commit()
        return paciente

    def update(self, paciente: Paciente) -> Paciente:
        self.session.commit()
        return paciente

    def delete(self, paciente_id: int) -> None:
        paciente = self.get(paciente_id)
        self.session.delete(paciente)
        self.session.commit()


class FakePacienteRepository(AbstractPacienteRepository):
    def __init__(self):
        self.pacientes = []

    def get(self, paciente_id: int) -> Paciente:
        for paciente in self.pacientes:
            if paciente.id == paciente_id:
                return paciente
        return None

    def get_all(self) -> List[Paciente]:
        return self.pacientes

    def create(self, paciente: Paciente) -> Paciente:
        self.pacientes.append(paciente)
        return paciente

    def update(self, paciente: Paciente) -> Paciente:
        for i, p in enumerate(self.pacientes):
            if p.id == paciente.id:
                self.pacientes[i] = paciente
                return paciente
        return None

    def delete(self, paciente_id: int) -> None:
        self.pacientes = [p for p in self.pacientes if p.id != paciente_id]