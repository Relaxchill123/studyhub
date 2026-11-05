from dotenv import load_dotenv
from dataclasses import dataclass, field
import os
from pathlib import Path
from app.exceptions import CookieSecureError

from sqlalchemy import URL
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def default_database_url(project_root: Path) -> str:
    path = (project_root / "data" / "planner.sqlite3").resolve()
    return URL.create("sqlite", database=path.as_posix()).render_as_string(
        hide_password=False
    )

def normalize_database_url(raw: str | None, project_root: Path) -> str:
    if raw is None:
        return default_database_url(project_root)
    if not raw.strip():
        raise ValueError("DATABASE_URL must not be empty")

    try:
        url = make_url(raw.strip())
    except ArgumentError as error:
        raise ValueError("DATABASE_URL must be a valid SQLite URL") from error

    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise ValueError("DATABASE_URL must point to a file-based SQLite database")

    path = Path(url.database)
    if not path.is_absolute():
        path = (project_root / path).resolve()
    return url.set(database=path.as_posix()).render_as_string(hide_password=False)

@dataclass
class Settings:
    json_path: Path
    app_name: str
    cookie_secure: bool
    database_url: str = field(
        default_factory=lambda: default_database_url(PROJECT_ROOT)
    )

def load_settings(environ=None, project_root=None):
    JSON_PATH = os.environ.get("JSON_PATH")
    
    if JSON_PATH is None:
        JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "tasks.json"
    else:
        JSON_PATH = Path(JSON_PATH)
    
    APP_NAME = os.environ.get("APP_NAME", "StudyHub Planner")

    COOKIE_SECURE = os.environ.get("COOKIE_SECURE")

    if COOKIE_SECURE is None:
        COOKIE_SECURE = False
    
    normalize_cookie_secure = COOKIE_SECURE.lower().strip()
    if normalize_cookie_secure == 'true':
        COOKIE_SECURE = True
    elif normalize_cookie_secure == 'false':
        COOKIE_SECURE = False
    else:
        raise CookieSecureError("Значение COOKIE_SECURE задано некорректно")

    db_url = normalize_database_url(os.environ.get("DATABASE_URL"), PROJECT_ROOT)


    return Settings(
        json_path=JSON_PATH,
        app_name=APP_NAME,
        cookie_secure=COOKIE_SECURE,
        database_url=db_url
    )