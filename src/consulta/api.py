from flask import Flask

from orm import metadata, start_mappers
from repositories import SqlAlchemyRepository

app = Flask(__name__)