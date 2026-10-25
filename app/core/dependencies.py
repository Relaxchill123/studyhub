from app.services import PlannerService
from fastapi import Request

def get_planner(request: Request) -> PlannerService:
    return request.app.state.planner
