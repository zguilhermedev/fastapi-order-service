from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.models.user import User
from app.db.session import get_db_session
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.customer_service import CustomerService
from app.services.product_service import ProductService

DbSession = Annotated[Session, Depends(get_db_session)]

bearer_scheme = HTTPBearer()


def get_product_repository(session: DbSession) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(session: DbSession) -> ProductService:
    repository = get_product_repository(session)
    return ProductService(repository)


def get_customer_repository(session: DbSession) -> CustomerRepository:
    return CustomerRepository(session)


def get_customer_service(session: DbSession) -> CustomerService:
    repository = get_customer_repository(session)
    return CustomerService(repository)


def get_user_repository(session: DbSession) -> UserRepository:
    return UserRepository(session)


def get_auth_service(session: DbSession) -> AuthService:
    repository = get_user_repository(session)
    return AuthService(repository)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: DbSession,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repository = UserRepository(session)
    user = user_repository.get_by_username(username)

    if user is None:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]