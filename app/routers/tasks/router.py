from typing import Annotated
from fastapi import Path, APIRouter, Request, HTTPException, Query
from app.routers.tasks.schemas import TaskCreate, TaskRead, TaskUpdate, TaskPatch
from app.exceptions import TaskNotFoundError

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskRead])
def tasks(
    request: Request,
    is_done: bool = None,
    limit: int = Query(default=10, ge=1, le=50),
    sort_desc: bool = False):

    public_tasks =[]

    for task in request.app.state.planner.select_tasks(is_done=is_done, limit=limit, sort_desc=sort_desc):
        public_tasks.append({
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'is_done': task.is_done,
        })

    return public_tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(request: Request, task_id: Annotated[int, Path(gt=0)]):
    try:
        task = request.app.state.planner.find_task(task_id)
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

@router.post("", status_code=201, response_model=TaskRead)
def post_task(request: Request, payload: TaskCreate):
    try:
        task = request.app.state.planner.add_task(payload.title, payload.priority)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return {
        'id': task.id,
        'title': task.title,
        'priority': task.priority,
        'is_done': task.is_done,
    }

@router.put("/{task_id}", status_code=200, response_model=TaskRead)
def put_task(request: Request, task_id: Annotated[int, Path(gt=0)], payload: TaskUpdate):
    try:
        task = request.app.state.planner.replace_task(task_id, payload.title, payload.priority, payload.is_done)
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
    except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

@router.patch("/{task_id}", response_model=TaskRead)
def put_task(request: Request, task_id: Annotated[int, Path(gt=0)], payload: TaskPatch):
    try:
        task = request.app.state.planner.patch_task(task_id, payload.title, payload.priority, payload.is_done)
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
    except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error


@router.delete("/{task_id}", status_code=204)
def delete_task(request: Request, task_id: Annotated[int, Path(gt=0)]):
    try:
        if task_id <= 0:
            raise HTTPException(status_code=422, detail="ID не может быть меньше 0")
        request.app.state.planner.remove_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(
                    status_code=404,
                    detail='Task not found',
                ) from error