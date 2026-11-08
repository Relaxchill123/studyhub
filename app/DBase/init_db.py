import app.DBase.models
from app.DBase.models import Base
from app.DBase.engine import make_engine
from app.core.config import load_settings

def main() -> None:
    settings = load_settings()
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()