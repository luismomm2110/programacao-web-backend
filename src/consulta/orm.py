from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import mapper, relationship, registry

from consulta.domain.models import model

metadata = MetaData()

medicos = Table(
    'medico', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50)),
    Column('crm', String(10))
)


pacientes = Table(
    'paciente', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50)),
    Column('cpf', String(11))
)

consultas = Table(
    'consulta', metadata,
    Column('id', Integer, primary_key=True),
    Column('medico_id', Integer, ForeignKey('medico.id')),
    Column('paciente_id', Integer, ForeignKey('paciente.id')),
    Column('horario', Date))


def start_mappers():
    reg = registry()

    reg.map_imperatively(model.Paciente, pacientes)
    reg.map_imperatively(model.Medico, medicos)
    reg.map_imperatively(model.Consulta, consultas, properties={
        'medico': relationship(model.Medico),
        'paciente': relationship(model.Paciente)
    })