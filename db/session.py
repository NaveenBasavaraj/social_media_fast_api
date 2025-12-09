# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings

# 1) Create a single shared Engine (thread-safe, uses connection pool)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # avoids dead connections
)

# 2) Session factory (not a single Session!)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# 3) Dependency for FastAPI: one Session per request
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
