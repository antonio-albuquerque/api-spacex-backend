from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

PG_USER = config("POSTGRES_USER", None)
PG_PASSWORD = config("POSTGRES_PASSWORD", None)
PG_HOST = config("POSTGRES_HOST", "localhost")
DATABASE = config("DATABASE", "api_space_x")
PG_PORT = config("POSTGRES_PORT", 5432, cast=int)
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{DATABASE}"

# if not all((PG_USER, PG_PASSWORD)):
#     raise MissingEnvVarsException(["PG_USER", "PG_PASSWORD"])

Base = declarative_base()


def get_engine():
    engine = create_engine(DB_URI, echo=True, future=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


engine = get_engine()

Session = sessionmaker(bind=engine)
