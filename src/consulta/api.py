from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import orm
from auth.auth_repository import SqlAlchemyAuthUserRepository
from consulta.repositories.paciente_repository import SqlAlchemyPacienteRepository
from services import services


engine = create_engine('postgresql://user:password@localhost:5432/consultas')
get_session = sessionmaker(bind=engine)
app = Flask(__name__)
CORS(app)
orm.start_mappers()
orm.metadata.create_all(engine)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
jwt = JWTManager(app)


@app.route('/criar_paciente', methods=['POST'])
def criar_paciente():
    session = get_session()
    auth_repository = SqlAlchemyAuthUserRepository(session)
    paciente_repository = SqlAlchemyPacienteRepository(session)
    try:
        paciente = services.criar_conta_paciente(
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
        return jsonify({"access_token": create_access_token(identity=user.id)}), 200
    return '', 401

if __name__ == '__main__':
    app.run(port=5000)
