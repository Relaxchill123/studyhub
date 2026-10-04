from fastapi import FastAPI
from app.main import build_service

app = FastAPI()
app.state.planner = build_service()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def tasks():
    public_tasks = []
    for task in app.state.planner.list_tasks():
        public_tasks.append({
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'is_done': task.is_done,
        })

    return public_tasks

@app.get("/stats")
def stats():
    stats = app.state.planner.get_stats()
    return {
        'total': stats['all'],
        'open': stats['open'],
        'done': stats['done'],
    }
     