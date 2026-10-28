from dotenv import load_dotenv
from dataclasses import dataclass
import os
from pathlib import Path

load_dotenv()

@dataclass
class Settings:
    json_path: Path
    app_name: str

def load_settings():
    JSON_PATH = os.environ.get("JSON_PATH")
    
    if JSON_PATH is None:
        JSON_PATH = Path(__file__).resolve().parents[1] / "data" / "tasks.json"

    JSON_PATH = Path(JSON_PATH)
    
    APP_NAME = os.environ.get("APP_NAME", "StudyHub Planner")
    return Settings(json_path=JSON_PATH, app_name=APP_NAME)