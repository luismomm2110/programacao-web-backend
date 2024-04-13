from typing import Type

from sqlalchemy.orm import Session

from auth.model import AuthUser

class AbstractAuthUserRepository:
    def get_user_by_email(self, email: str) -> Type[AuthUser] | None:
        raise NotImplementedError

    def add(self, user: AuthUser) -> None:
        raise NotImplementedError


class SqlAlchemyAuthUserRepository(AbstractAuthUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> Type[AuthUser] | None:
        return self.session.query(AuthUser).filter_by(email=email).first()

    def add(self, user: AuthUser) -> None:
        self.session.add(user)


class FakeAuthUserRepository(AbstractAuthUserRepository):
    def __init__(self):
        self.users = []

    def get_user_by_email(self, email: str) -> Type[AuthUser] | None:
        for user in self.users:
            if user.email == email:
                return user

    def add(self, user: AuthUser) -> None:
        self.users.append(user)