from abc import abstractmethod, ABC
from datetime import date, datetime
from typing import List

from consulta.domain.models.model import Consulta


class AbstractConsultaRepository(ABC):
    def __init__(self):
        self.seen = set()

    def get(self, consulta_id: str) -> Consulta:
        consulta = self._get(consulta_id)
        if consulta:
            self.seen.add(consulta)
        return consulta
    
    @abstractmethod
    def _get(self, consulta_id: str) -> Consulta:
        raise NotImplementedError

    @abstractmethod
    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        pass

    @abstractmethod
    def get_by_paciente_id(self, paciente_id: int) -> List[Consulta]:
        pass

    def add(self, consulta: Consulta) -> None:
        self._add(consulta)
        self.seen.add(consulta)

    @abstractmethod
    def _add(self, consulta: Consulta) -> None:
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

    @abstractmethod
    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        pass


class SqlAlchemyConsultaRepository(AbstractConsultaRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _get(self, consulta_id: str) -> Consulta:
        return self.session.query(Consulta).filter_by(id=consulta_id).first()

    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        consulta = self.session.query(Consulta).filter_by(medico_id=medico_id).all()
        if consulta:
            self.seen.add(consulta)
            return consulta
        return []

    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        consultas = self.session.query(Consulta).filter_by(paciente_id=paciente_id).all()
        if consultas:
            for consulta in consultas:
                self.seen.add(consulta)
            return consultas
        return []

    def _add(self, consulta: Consulta) -> None:
        self.session.add(consulta)

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
        super().__init__()
        self._consultas = []

    def _get(self, consulta_id: str) -> Consulta:
        for consulta in self._consultas:
            if consulta.id == consulta_id:
                return consulta
        return None

    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        consultas = [consulta for consulta in self._consultas if consulta.paciente_id == paciente_id]
        self.seen.update(consultas)
        return consultas


    def get_by_medico_id(self, medico_id: str) -> List[Consulta]:
        consultas = [consulta for consulta in self._consultas if consulta.medico_id == medico_id]
        self.seen.update(consultas)
        return consultas

    def _add(self, consulta: Consulta) -> None:
        self._consultas.append(consulta)

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
        return self._consultas
    
    def get_by_paciente_id(self, paciente_id: str) -> List[Consulta]:
        consultas = [consulta for consulta in self._consultas if consulta.paciente_id == paciente_id]
        self.seen.update(consultas)
        return consultas