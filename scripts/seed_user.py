from sqlalchemy import select

from app.core.security import hash_password
from app.db.models.user import User
from app.db.session import SessionLocal


def main() -> None:
    session = SessionLocal()

    try:
        existing_user = session.scalar(
            select(User).where(User.username == "admin")
        )

        if existing_user:
            print("User 'admin' already exists.")
            return

        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            is_active=True,
        )

        session.add(user)
        session.commit()
        print("User 'admin' created successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()