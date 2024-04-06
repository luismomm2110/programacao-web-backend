from flask import Flask, request, jsonify
from flask_cors import CORS
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

if __name__ == '__main__':
    app.run(port=5000)
