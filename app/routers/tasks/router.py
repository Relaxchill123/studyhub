from typing import Annotated
from fastapi import Path, APIRouter, HTTPException, Query, Depends, Header, Response
from app.routers.tasks.schemas import TaskCreate, TaskRead, TaskUpdate, TaskPatch
from app.exceptions import TaskNotFoundError
from app.core.dependencies import PlannerDep, SelectionParams, get_selected_tasks
from app.services import PlannerService

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskId = Annotated[int, Path(gt=0)]

@router.get("", response_model=list[TaskRead])
def tasks(
    selection: Annotated[SelectionParams, Depends(get_selected_tasks)]
    ):

    public_tasks = []

    for task in selection:
        public_tasks.append({
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'is_done': task.is_done,
        })

    return public_tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: TaskId,
    planner: PlannerDep,
    ):

    try:
        task = planner.find_task(task_id)
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
def post_task(payload: TaskCreate, planner: PlannerDep):
    try:
        task = planner.add_task(payload.title, payload.priority)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return {
        'id': task.id,
        'title': task.title,
        'priority': task.priority,
        'is_done': task.is_done,
    }

@router.put("/{task_id}", status_code=200, response_model=TaskRead)
def put_task(task_id: TaskId, payload: TaskUpdate, planner: PlannerDep):
    try:
        task = planner.replace_task(task_id, payload.title, payload.priority, payload.is_done)
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
def put_task(task_id: TaskId, payload: TaskPatch, planner: PlannerDep):
    try:
        task = planner.patch_task(task_id, payload.title, payload.priority, payload.is_done)
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
def delete_task(task_id: TaskId, planner: PlannerDep):
    try:
        if task_id <= 0:
            raise HTTPException(status_code=422, detail="ID не может быть меньше 0")
        planner.remove_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(
                    status_code=404,
                    detail='Task not found',
                ) from error