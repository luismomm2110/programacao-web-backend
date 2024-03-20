from datetime import datetime

import pytest

from consulta.domain.models.model import Medico, Paciente


def test_deve_marcar_horario_preenchido_na_agenda_do_medico():
    medico = Medico(nome='Luisa', crm='1234')
    paciente = Paciente(nome='Maria', cpf='12345678901')

    medico.agendar_consulta(
        paciente,
        datetime(2021, 1, 1, 8, 0)
    )

    assert medico.agenda == {
        datetime(
            2021, 1, 1, 8, 0
        ): paciente
    }


def test_pode_marcar_horario_disponivel_na_agenda_do_medico():
    medico = Medico(nome='Luisa', crm='1234')

    assert medico.pode_agendar_consulta(datetime(2021, 1, 1, 8, 0))


def test_nao_pode_marcar_horario_preenchido_na_agenda_do_medico():
    medico = Medico(nome='Luisa', crm='1234')
    paciente = Paciente(nome='Maria', cpf='12345678901')

    medico.agendar_consulta(paciente, datetime(2021, 1, 1, 8, 0))

    assert not medico.pode_agendar_consulta(datetime(2021, 1, 1, 8, 0))


def test_deve_liberar_horario_quando_cancelar_consulta():
    medico = Medico(nome='Luisa', crm='1234')
    paciente = Paciente(nome='Maria', cpf='12345678901')

    medico.agendar_consulta(paciente, datetime(2021, 1, 1, 8, 0))
    medico.cancelar_consulta(datetime(2021, 1, 1, 8, 0))

    assert medico.agenda == {}
