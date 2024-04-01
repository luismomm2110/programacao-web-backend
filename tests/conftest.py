import sys
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from consulta.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
