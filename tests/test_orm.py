from datetime import date

import pytest
from sqlalchemy import text

from consulta.domain.models import model


## TODO deletar


def test_paciente_mapper_consegue_salvar_no_banco_de_dados(session):
    session.execute(
        text(
            'INSERT INTO paciente (nome, cpf) VALUES (:nome, :cpf)'
        ),
        {'nome': 'Luis', 'cpf': '08837535961'}
    )
    expected = model.Paciente('Luis', '08837535961')

    result = session.query(model.Paciente).one()
    assert result == expected


def test_medico_mapper_consegue_salvar_no_banco_de_dados(session):
    session.execute(
        text(
            'INSERT INTO medico (nome, crm) VALUES (:nome, :crm)'
        ),
        {'nome': 'Dr. House', 'crm': '123456'}
    )
    expected = model.Medico('Dr. House', '123456')

    result = session.query(model.Medico).one()
    assert result == expected


def test_consulta_mapper_consegue_salvar_no_banco_de_dados(session):
    session.execute(
        text(
            'INSERT INTO medico (nome, crm) VALUES (:nome, :crm)'
        ),
        {'nome': 'Dr. House', 'crm': '123456'}
    )
    session.execute(
        text(
            'INSERT INTO paciente (nome, cpf) VALUES (:nome, :cpf)'
        ),
        {'nome': 'Luis', 'cpf': '08837535961'}
    )

    session.execute(
        text(
            'INSERT INTO consulta (medico_id, paciente_id, horario) VALUES (:medico_id, :paciente_id, :horario)'
        ),
        {'medico_id': 1, 'paciente_id': 1, 'horario': '2021-10-10'}
    )

    expected = model.Consulta(1, 1, date(2021, 10, 10))
    assert session.query(model.Consulta).one() == expected
