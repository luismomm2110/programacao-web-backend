from datetime import datetime

from consulta.domain.models.model import Medico, Paciente, agendar_consulta, Consulta


def test_deve_marcar_horario_preenchido_na_agenda_do_medico():
    medico, paciente = criar_medico_e_paciente()

    agendar_consulta(
        medico,
        paciente.id,
        datetime(2021, 1, 1, 8, 0)
    )

    assert medico.agenda == {
        datetime(
            2021, 1, 1, 8, 0
        ): Consulta(
            medico_id=medico.id,
            paciente_id=paciente.id,
            horario=datetime(2021, 1, 1, 8, 0)
        )
    }


def test_deve_retornar_horario_indisponivel_quando_nao_pode_agendar_consulta():
    data = datetime(2021, 1, 1, 8, 0)
    medico, paciente = criar_medico_e_paciente()

    agendar_consulta(
        medico,
        paciente,
        data,
    )
    erro = agendar_consulta(
        medico,
        paciente,
        data,
    )

    assert erro == 'Horário indisponível'


def criar_medico_e_paciente():
    medico = Medico(nome='Luisa', crm='1234')
    paciente = Paciente(nome='Maria', cpf='12345678901')
    return medico, paciente
