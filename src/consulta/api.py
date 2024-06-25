from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import consulta.services.pacientes_services
import consulta.orm as orm
from auth import auth_repository
from auth.auth_repository import SqlAlchemyAuthUserRepository
from consulta.adapters.rabbitmq_eventpublisher import RabbitMQEventPublisher
from consulta.domain.events.events import ConsultaCancelada, ConsultaCriada
from consulta.repositories.medico_repository import SqlAlchemyMedicoRepository
from consulta.repositories.paciente_repository import SqlAlchemyPacienteRepository
from consulta.services import unit_of_work
from consulta.services.consulta_services import marcar_consulta
from consulta.services.medicos_services import criar_medico


import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

connection_string = 'postgresql+psycopg2://postgres:postgres@localhost/consultas'
logger.debug(f"Creating engine with connection string: {connection_string}")
engine = create_engine(connection_string)
get_session = sessionmaker(bind=engine, expire_on_commit=False)
app = Flask(__name__)
orm.start_mappers()
orm.metadata.create_all(engine)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
ewt = JWTManager(app)

CORS(app, suports_credentials=True)


@app.route('/medicos', methods=['GET'])
def listar_medicos():
    session = get_session()
    medico_repository = SqlAlchemyMedicoRepository(session)
    medicos = medico_repository.get_all()
    return [medico.to_json() for medico in medicos]


@app.route('/medicos', methods=['POST'])
def cria_medico():
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    try:
        medico = criar_medico(
            request.json['nome'],
            request.json['crm'],
            uow
        )
    except ValueError as e:
        return str(e), 400
    return jsonify({"id": medico['id']}), 201


@app.route('/pacientes', methods=['POST'])
def criar_paciente():
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    try:
        paciente = consulta.services.pacientes_services.criar_conta_paciente(
            request.json,
            uow
        )
    except ValueError as e:
        return str(e), 400
    return jsonify({"id": paciente.id}), 201


@app.route('/login', methods=['POST'])
def login():
    session = get_session()
    auth_repository = SqlAlchemyAuthUserRepository(session)
    user = auth_repository.get_user_by_email(request.json['email'])
    if user and user.password == request.json['password']:
        return jsonify({"token": create_access_token(identity=user.id), "id": user.id}), 200
    return '', 401


@app.route('/consultas', methods=['GET'])
def listar_consultas():
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    consultas = []
    with uow:
        consultas = uow.consultas.list()
        return jsonify([consulta for consulta in consultas])


@app.route('/consultas', methods=['POST'])
@jwt_required()
def criar_consulta():
    session = get_session()
    auth_repository = SqlAlchemyAuthUserRepository(session)
    auth_id = get_jwt_identity()
    email_paciente = auth_repository.get_user_by_id(auth_id).email
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    consulta_id = marcar_consulta(
        {
            **request.json,
            'email': email_paciente
        },
        uow
    )
    return jsonify({"id": consulta_id}), 201


@app.route('/pacientes/<int:user_id>/consultas', methods=['GET'])
def listar_consultas_paciente(user_id):
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    auth_user_repository = SqlAlchemyAuthUserRepository(session)
    user = auth_user_repository.get_user_by_id(user_id)
    consultas_retornadas = []
    with uow:
        consultas = uow.consultas.get_by_paciente_id(user.entity_id)
        for consulta in consultas:
            consulta_json = consulta.to_json()
            consulta_json['medico'] = uow.medicos.get(consulta_json['medico_id']).to_json()
            consultas_retornadas.append(consulta_json)
        return jsonify(consultas_retornadas)


@app.route('/medicos/<int:user_id>/consultas', methods=['GET'])
def listar_consultas_medico(user_id):
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    consultas_retornadas = []
    with uow:
        consultas = uow.consultas.get_by_medico_id(user_id)
        medico = uow.medicos.get(user_id)
        for consulta in consultas:
            consulta_json = consulta.to_json()
            consulta_json['paciente'] = uow.pacientes.get(consulta_json['paciente_id']).to_json()
            consultas_retornadas.append(consulta_json)
        ## return consultas_retornadas and nome
        return {"consultas": consultas_retornadas, "nome": medico.nome}

@app.route('/consultas/<int:consulta_id>', methods=['DELETE'])
def deletar_consulta(consulta_id):
    session = get_session()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session)
    with uow:
        uow.consultas.delete(consulta_id)
        try:
            rabbitmq = RabbitMQEventPublisher('localhost')
            rabbitmq.publish(ConsultaCancelada(
                consulta_id=consulta_id
            ).to_json())
        except Exception as e:
            print(e)
            pass
    return '', 204

    
@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    session = get_session()
    paciente_repository = SqlAlchemyPacienteRepository(session)
    pacientes = paciente_repository.get_all()
    return [paciente.to_json() for paciente in pacientes]

if __name__ == '__main__':
    app.run(port=5000)
