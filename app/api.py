from fastapi import FastAPI, HTTPException, Query
from app.main import build_service
from app.exceptions import TaskNotFoundError
from pydantic import BaseModel

app = FastAPI()
app.state.planner = build_service()

class TaskCreate(BaseModel):
    title: str
    priority: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def tasks(
    is_done: bool = None,
    limit: int = Query(default=10, ge=1, le=50),
    sort_desc: bool = False):

    return app.state.planner.select_tasks(is_done=is_done, limit=limit, sort_desc=sort_desc)

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
            detail='Task not found',
        ) from error

@app.post("/tasks", status_code=201)
def post_task(payload: TaskCreate):
    try:
        app.state.planner.add_task(payload.title, payload.priority)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return app.state.planner.find_task