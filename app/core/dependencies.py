from app.services import PlannerService
from fastapi import Request, Depends
from typing import Annotated

def get_planner(request: Request) -> PlannerService:
    return request.app.state.planner

PlannerDep = Annotated[
    PlannerService,
    Depends(get_planner),
]