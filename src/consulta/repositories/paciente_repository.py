from abc import ABC, abstractmethod
from typing import List

from consulta.domain.models.model import Paciente


class AbstractPacienteRepository(ABC):
    @abstractmethod
    def get_paciente(self, paciente_id: int) -> Paciente:
        pass

    @abstractmethod
    def get_pacientes(self) -> List[Paciente]:
        pass

    @abstractmethod
    def create_paciente(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def update_paciente(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def delete_paciente(self, paciente_id: int) -> None:
        pass

class SqlAlchemyPacienteRepository(AbstractPacienteRepository):
    def __init__(self, session):
        self.session = session

    def get_paciente(self, paciente_id: int) -> Paciente:
        return self.session.query(Paciente).filter_by(id=paciente_id).first()

    def get_pacientes(self) -> List[Paciente]:
        return self.session.query(Paciente).all()

    def create_paciente(self, paciente: Paciente) -> Paciente:
        self.session.add(paciente)
        self.session.commit()
        return paciente

    def update_paciente(self, paciente: Paciente) -> Paciente:
        self.session.commit()
        return paciente

    def delete_paciente(self, paciente_id: int) -> None:
        paciente = self.get_paciente(paciente_id)
        self.session.delete(paciente)
        self.session.commit()


class FakePacienteRepository(AbstractPacienteRepository):
    def __init__(self):
        self.pacientes = []

    def get_paciente(self, paciente_id: int) -> Paciente:
        for paciente in self.pacientes:
            if paciente.id == paciente_id:
                return paciente
        return None

    def get_pacientes(self) -> List[Paciente]:
        return self.pacientes

    def create_paciente(self, paciente: Paciente) -> Paciente:
        self.pacientes.append(paciente)
        return paciente

    def update_paciente(self, paciente: Paciente) -> Paciente:
        for i, p in enumerate(self.pacientes):
            if p.id == paciente.id:
                self.pacientes[i] = paciente
                return paciente
        return None

    def delete_paciente(self, paciente_id: int) -> None:
        self.pacientes = [p for p in self.pacientes if p.id != paciente_id]