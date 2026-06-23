from sqlalchemy.orm import Session

from app.core.database import get_db


def test_get_db_yields_session() -> None:
    session = next(get_db())

    try:
        assert isinstance(session, Session)
    finally:
        session.close()
