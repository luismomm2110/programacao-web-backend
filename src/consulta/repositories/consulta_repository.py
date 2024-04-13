from abc import abstractmethod, ABC
from typing import List

from consulta.domain.models.model import Consulta


class AbstractConsultaRepository(ABC):
    @abstractmethod
    def get(self, consulta_id: str) -> Consulta:
        pass

    @abstractmethod
    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        pass

    @abstractmethod
    def get_by_paciente_id(self, paciente_id: int) -> List[Consulta]:
        pass

    @abstractmethod
    def add(self, consulta: Consulta) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Consulta]:
        pass

    @abstractmethod
    def update(self, consulta: Consulta) -> None:
        pass

    @abstractmethod
    def delete(self, consulta_id: str) -> None:
        pass

    @abstractmethod
    def get_all(self):
        pass


class SqlAlchemyConsultaRepository(AbstractConsultaRepository):

    def __init__(self, session):
        self.session = session

    def get(self, consulta_id: str) -> Consulta:
        return self.session.query(Consulta).filter_by(id=consulta_id).first()

    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        return self.session.query(Consulta).filter_by(medico_id=medico_id).all()

    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        return self.session.query(Consulta).filter_by(paciente_id=paciente_id).all()

    def add(self, consulta: Consulta) -> None:
        self.session.add(consulta)
        self.session.commit()

    def list(self) -> List[Consulta]:
        return self.session.query(Consulta).all()

    def update(self, consulta: Consulta) -> None:
        self.session.commit()

    def delete(self, consulta_id: str) -> None:
        consulta = self.get(consulta_id)
        self.session.delete(consulta)
        self.session.commit()

    def get_all(self):
        return self.session.query(Consulta).all()

class FakeConsultaRepository(AbstractConsultaRepository):
    def __init__(self):
        self.consultas = []

    def get(self, consulta_id: str) -> Consulta:
        for consulta in self.consultas:
            if consulta.id == consulta_id:
                return consulta

    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        return [consulta for consulta in self.consultas if consulta.paciente_id == paciente_id]

    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        return [consulta for consulta in self.consultas if consulta.medico_id == medico_id]

    def add(self, consulta: Consulta) -> None:
        self.consultas.append(consulta)

    def list(self) -> List[Consulta]:
        return self.consultas

    def update(self, consulta: Consulta) -> None:
        for i, c in enumerate(self.consultas):
            if c.id == consulta.id:
                self.consultas[i] = consulta

    def delete(self, consulta_id: str) -> None:
        for i, c in enumerate(self.consultas):
            if c.id == consulta_id:
                del self.consultas[i]
                break

    def get_all(self):
        return self.consultas