from typing import Type

from sqlalchemy.orm import Session

from auth.model import User


class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> Type[User] | None:
        return self.session.query(User).filter_by(email=email).first()

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
