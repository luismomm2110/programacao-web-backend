from sqlalchemy import MetaData, Integer, Column, String, Table
from sqlalchemy.orm import registry

from auth import model

metadata = MetaData()


users = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
    Column('password', String(50)),
    Column('entity_id', Integer)
)

def start_mappers():
    reg = registry()

    reg.map_imperatively(model.User, users)


