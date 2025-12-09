# Social Media App Using Fast Api

# Social Media App — FastAPI (Beginner Guide)

This is a simple social-media-style backend built with FastAPI and SQLAlchemy. The goal of this README is to explain the project "like you're a noob": why things exist, how they connect, how to run the project (locally and with Docker), and how to troubleshoot common errors.

Contents

- Project purpose and high-level flow
- Prerequisites
- Quick start (local & Docker)
- Important files explained (with code snippets)
- Common errors and fixes
- Next steps (recommended improvements)

Prerequisites

- Python 3.11+ (project uses Python 3.12 in the virtualenv but 3.11+ is fine)
- Docker & docker-compose (if you want to run the app with PostgreSQL in containers)

Quick start — local (venv)

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv fenv
& .\fenv\Scripts\Activate.ps1
```

2. Install dependencies and save them:

```powershell
pip install -r requirements.txt
# OR when starting from scratch:
pip install "fastapi[all]" psycopg2-binary
pip freeze > requirements.txt
```

3. Provide environment variables in a `.env` file at the project root. An example minimal `.env` for Docker (used by `docker-compose.yml`):

```text
# .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres
# If you run locally without Docker, set host to localhost and port to 5432
# DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres
```

4. Run the app locally (development):

```powershell
# from project root
uvicorn main:app --reload
```

Quick start — Docker (recommended for reproducible DB)

1. Build and run the services with `docker-compose` (this runs a PostgreSQL container named `db` and the FastAPI `app` container):

```powershell
docker-compose down
docker-compose up --build
# or detached:
# docker-compose up --build -d
```

2. View logs (helpful for debugging startup/database errors):

```powershell
docker-compose logs -f app
```

Why you might see "relation \"posts\" does not exist"

- That error means your application attempted to query a table that doesn't exist in the database yet.
- Typical causes:
  - You haven't created the tables (either via SQLAlchemy's `create_all` or with migrations like Alembic).
  - The app tried to query before the database container was fully ready.

This project uses SQLAlchemy models and a startup hook to create missing tables automatically. The relevant code (in `main.py`) looks like:

```python
import models  # ensures model classes are imported and registered with Base
from db.base import Base
from db.session import engine
import time
from sqlalchemy.exc import OperationalError

@app.on_event("startup")
def on_startup():
        # Wait for DB to be reachable (useful in Docker)
        max_tries = 10
        for attempt in range(1, max_tries + 1):
                try:
                        with engine.connect():
                                break
                except OperationalError:
                        if attempt == max_tries:
                                raise
                        time.sleep(2)

        Base.metadata.create_all(bind=engine)
```

Important files explained (what they do)

- `main.py` — FastAPI entry point

  - Includes routers and registers a startup event that creates DB tables if needed.

- `db/base.py` — SQLAlchemy base class

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

- `db/session.py` — Engine & Session factory

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()
```

- `models/user.py` and `models/post.py` — example SQLAlchemy models

`models/user.py` excerpt:

```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from db.base import Base
from sqlalchemy.sql import func

class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, nullable=False)
        username = Column(String, unique=True, nullable=True)
        hashed_password = Column(String, nullable=False)
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
```

`models/post.py` excerpt:

```python
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.sql import func

class Post(Base):
        __tablename__ = "posts"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String, nullable=False)
        content = Column(String, nullable=False)
        owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        published = Column(Boolean, default=True)

        owner = relationship("User", backref="posts")
```

- `routers/posts.py` — request handlers for posts

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.post import Post

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list)
def get_posts(db: Session = Depends(get_db)):
        return db.query(Post).all()

@router.post("/", status_code=201)
def create_post(post_data, db: Session = Depends(get_db)):
        new_post = Post(...)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
```

Common errors & troubleshooting

- Error: `sqlalchemy.exc.ProgrammingError: relation "posts" does not exist`
  - Cause: the `posts` table hasn't been created in the database.
  - Quick fixes:
    - Ensure your `.env` sets `DATABASE_URL` correctly for the environment you're running in.
    - If running with Docker, run `docker-compose up --build` so the app runs inside the same network where host `db` resolves.
    - Check `docker-compose logs -f app` for errors during startup.
    - Run the create-tables script manually from within the project's virtualenv (note: this will try to connect to the DB hostname in `DATABASE_URL`):

```powershell
& .\fenv\Scripts\Activate.ps1
python -c "from db.base import Base; from db.session import engine; import models; Base.metadata.create_all(bind=engine); print('OK: created')"
```

    - Note: Running the single-line creation locally may fail if `DATABASE_URL` uses `db` as the host (that's a Docker service name). Replace the host with `localhost` when creating tables against a local Postgres instance.

- Error: `could not translate host name "db" to address`
  - Cause: hostname `db` exists only in the Docker network. When running outside Docker, use `localhost` in `DATABASE_URL`.

API examples

- Get posts:

```bash
curl http://localhost:8000/posts/
```

- Create a post (example JSON):

```bash
curl -X POST http://localhost:8000/posts/ \
    -H "Content-Type: application/json" \
    -d '{"title": "Hello", "content": "World"}'
```

Next steps / improvements

- Use Alembic for migrations instead of `create_all` (recommended for production)
- Add a `healthcheck` to the `db` service in `docker-compose.yml` and/or an init-wait script so the app waits for DB readiness more robustly.
- Add authentication and replace the hardcoded `fake_user_id` in `routers/posts.py` with real user IDs from login.
