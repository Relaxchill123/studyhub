from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def create_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine)