from abc import abstractmethod, ABC
from typing import List

from consulta.domain.models.model import Medico


class AbstractMedicoRepository(ABC):
    @abstractmethod
    def get(self, medico_id: int) -> Medico:
        pass

    @abstractmethod
    def get_medicos(self) -> List[Medico]:
        pass

    @abstractmethod
    def add(self, medico: Medico) -> Medico:
        pass

    @abstractmethod
    def update(self, medico: Medico) -> Medico:
        pass

    @abstractmethod
    def delete(self, medico_id: int) -> None:
        pass


class SqlAlchemyMedicoRepository(AbstractMedicoRepository):
    def __init__(self, session):
        self.session = session

    def get(self, medico_id: int) -> Medico:
        return self.session.query(Medico).filter_by(id=medico_id).first()

    def get_medicos(self) -> List[Medico]:
        return self.session.query(Medico).all()

    def add(self, medico: Medico) -> Medico:
        self.session.add(medico)
        self.session.commit()
        return medico

    def update(self, medico: Medico) -> Medico:
        self.session.commit()
        return medico

    def delete(self, medico_id: int) -> None:
        medico = self.get(medico_id)
        self.session.delete(medico)
        self.session.commit()


class FakeMedicoRepository(AbstractMedicoRepository):
    def __init__(self):
        self.medicos = []

    def get(self, medico_id: int) -> Medico:
        for medico in self.medicos:
            if medico.id == medico_id:
                return medico

    def get_medicos(self) -> List[Medico]:
        return self.medicos

    def add(self, medico: Medico) -> Medico:
        self.medicos.append(medico)
        return medico

    def update(self, medico: Medico) -> Medico:
        for i, m in enumerate(self.medicos):
            if m.id == medico.id:
                self.medicos[i] = medico
                return medico

    def delete(self, medico_id: int) -> None:
        for i, medico in enumerate(self.medicos):
            if medico.id == medico_id:
                del self.medicos[i]
                break
