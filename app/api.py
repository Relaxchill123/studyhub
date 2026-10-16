from fastapi import FastAPI
from app.main import build_service
from routers.tasks import router

app = FastAPI()
app.state.planner = build_service()
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