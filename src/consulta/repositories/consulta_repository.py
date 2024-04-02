from abc import abstractmethod, ABC
from typing import List

from consulta.domain.models.model import Consulta


class AbstractConsultaRepository(ABC):
    @abstractmethod
    def get(self, consulta_id: str) -> Consulta:
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


class SqlAlchemyConsultaRepository(AbstractConsultaRepository):
    def __init__(self, session):
        self.session = session

    def get(self, consulta_id: str) -> Consulta:
        return self.session.query(Consulta).filter_by(id=consulta_id).first()

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

class FakeConsultaRepository(AbstractConsultaRepository):
    def __init__(self):
        self.consultas = []

    def get(self, consulta_id: str) -> Consulta:
        for consulta in self.consultas:
            if consulta.id == consulta_id:
                return consulta

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
