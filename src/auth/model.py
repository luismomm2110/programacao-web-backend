from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash


class User():
    def __init__(self, username, password, entity_id):
        self.id = uuid4()
        self.username = username
        self.password = generate_password_hash(password)
        self.entity_id = entity_id

    def __repr__(self):
        return f'<User {self.username}>'

