import app.DBase.models
from app.DBase.models import TaskBase
from app.DBase.engine import create_engine
from app.core.config import load_settings

def main() -> None:
    settings = load_settings()
    engine = create_engine(settings.database_url)
    TaskBase.metadata.create_all(engine)


if __name__ == "__main__":
    main()