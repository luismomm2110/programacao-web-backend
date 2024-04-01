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