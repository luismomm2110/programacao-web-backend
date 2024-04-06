from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash


class AuthUser():
    def __init__(self, user_id, username, password, entity_id):
        self.id = user_id
        self.username = username
        self.password = password
        self.entity_id = entity_id

    def __repr__(self):
        return f'<User {self.username}>'

