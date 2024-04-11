import random

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import consulta.services.pacientes_services
import orm
from auth.auth_repository import SqlAlchemyAuthUserRepository
from consulta.domain.models.model import Medico
from consulta.repositories.medico_repository import SqlAlchemyMedicoRepository
from consulta.repositories.paciente_repository import SqlAlchemyPacienteRepository
from consulta.services.medicos_services import criar_medico
from services import consulta_services


engine = create_engine('postgresql://user:password@localhost:5432/consultas')
get_session = sessionmaker(bind=engine)
app = Flask(__name__)
orm.start_mappers()
orm.metadata.create_all(engine)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
jwt = JWTManager(app)

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
    medico_repository = SqlAlchemyMedicoRepository(session)
    try:
        medico = criar_medico(
            session,
            medico_repository,
            request.json['nome'],
            request.json['crm']
        )
    except ValueError as e:
        return str(e), 400
    return jsonify({"id": medico.id}), 201


@app.route('/paciente', methods=['POST'])
def criar_paciente():
    session = get_session()
    auth_repository = SqlAlchemyAuthUserRepository(session)
    paciente_repository = SqlAlchemyPacienteRepository(session)
    try:
        paciente = consulta.services.pacientes_services.criar_conta_paciente(
            auth_repository,
            paciente_repository,
            request.json,
            session
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
        return jsonify({"token": create_access_token(identity=user.id)}), 200
    return '', 401


if __name__ == '__main__':
    app.run(port=5000)
