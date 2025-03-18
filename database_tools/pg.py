from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session


def create_session(user: str, password: str, host: str, port: str, db: str) -> sessionmaker:
    engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        quote(user),
        quote(password),
        host,
        port,
        quote(db)
    ), echo=False, future=True, pool_size=50, max_overflow=0, connect_args={"options": "-c timezone=utc"})
    return sessionmaker(bind=engine)


class PostgresClient:
    BasePostgresModel = declarative_base()

    def __init__(self, user: str, password: str, host: str, port: str, db: str):
        self.__session = scoped_session(create_session(user, password, host, port, db))

    def __enter__(self):
        return self.__session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.remove()

    def close(self):
        self.__session.close()

    def get_session(self):
        return self.__session()


postgres_client = PostgresClient()
