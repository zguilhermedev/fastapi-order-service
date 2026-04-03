from app.core.security import create_access_token, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.user_repository.get_by_username(username)

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def login(self, username: str, password: str) -> str | None:
        user = self.authenticate_user(username, password)

        if user is None:
            return None

        return create_access_token(subject=user.username)