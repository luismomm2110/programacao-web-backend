#!/bin/sh

# Run docker-compose
docker-compose up -d

export PYTHONPATH="${PYTHONPATH}:/home/luismomm/Docs/Pessoal/Catolica/programacao-web/programacao-web-backend/src"

cd /home/luismomm/Docs/Pessoal/Catolica/programacao-web/programacao-web-backend/src/consulta

# Run the application
python3 api.py