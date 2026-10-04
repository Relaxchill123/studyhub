from fastapi import FastAPI, HTTPException
from app.main import build_service
from app.exceptions import TaskNotFoundError

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

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    try:
        task = app.state.planner.find_task(task_id)
        return {
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'is_done': task.is_done,
        }
    except TaskNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail='Task not found'
        ) from error