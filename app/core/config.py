from dotenv import load_dotenv
from dataclasses import dataclass
import os
from pathlib import Path
from app.exceptions import CookieSecureError

load_dotenv()

@dataclass
class Settings:
    json_path: Path
    app_name: str
    cookie_secure: bool

def load_settings():
    JSON_PATH = os.environ.get("JSON_PATH")
    
    if JSON_PATH is None:
        JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "tasks.json"
    else:
        JSON_PATH = Path(JSON_PATH)
    
    APP_NAME = os.environ.get("APP_NAME", "StudyHub Planner")

    COOKIE_SECURE = os.environ.get("COOKIE_SECURE")

    if COOKIE_SECURE:
        normalize_cookie_secure = COOKIE_SECURE.lower().strip()
        if normalize_cookie_secure == 'true':
            COOKIE_SECURE = True
        elif normalize_cookie_secure == 'false':
            COOKIE_SECURE = False
        else:
            raise CookieSecureError("Значение COOKIE_SECURE задано некорректно")
    else:
        COOKIE_SECURE = False


    return Settings(json_path=JSON_PATH, app_name=APP_NAME, cookie_secure=COOKIE_SECURE)