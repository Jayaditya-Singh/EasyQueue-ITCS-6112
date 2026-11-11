from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create backend/.env with "
        "DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/easyqueue"
    )

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite is only used by the test suite. An in-memory database must share
    # one connection across threads or each request would see an empty DB.
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    if DATABASE_URL in ("sqlite://", "sqlite:///:memory:"):
        engine_kwargs["poolclass"] = StaticPool
else:
    # Recycle dropped MySQL connections instead of failing the next request
    engine_kwargs["pool_pre_ping"] = True

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
