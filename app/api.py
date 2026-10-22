from fastapi import FastAPI
from app.main import build_service
from app.routers.tasks.router import router
from app.core.config import load_settings

settings = load_settings()
app = FastAPI(title=settings.app_name)
app.state.planner = build_service(settings)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats")
def stats():
    stats = app.state.planner.get_stats()
    return {
        'total': stats['all'],
        'open': stats['open'],
        'done': stats['done'],
    }