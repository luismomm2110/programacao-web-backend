from typing import Type

from sqlalchemy.orm import Session

from auth.model import AuthUser


class SqlAlchemyAuthUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> Type[AuthUser] | None:
        return self.session.query(AuthUser).filter_by(email=email).first()

    def add(self, user: AuthUser) -> None:
        self.session.add(user)
