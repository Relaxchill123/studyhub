from typing import Annotated
from fastapi import APIRouter, Header, Response, Cookie, status
from app.routers.preferences.schemas import PreferenceWrite, PreferenceRead

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.get("", response_model = PreferenceRead)
def read_preferences(
    response: Response,
    planner_view : str | None = Cookie(default=None),
    client_version: Annotated[
            str | None,
            Header(alias='X-Client-Version', max_length=64),
        ] = None,
) -> PreferenceRead:
    response.headers['X-Planner-Version'] = "1"

    view = planner_view if planner_view in {'detailed', 'compact'} else 'compact'
    
    if client_version is None:
        client_version = None
    
    return PreferenceRead(view=view, client_version=client_version)

@router.put("", response_model = PreferenceRead)
def update_preferences(
    response: Response,
    payload: PreferenceWrite,
    client_version: Annotated[
            str | None,
            Header(alias='X-Client-Version', max_length=64),
        ] = None,
) -> PreferenceRead:
    
    response.headers['X-Planner-Version'] = "1"

    # if payload is None

    response.set_cookie(
        key="planer_view",
        value=payload.view,
        path="/preferences",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return PreferenceRead(view=payload.view, client_version=client_version)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def update_preferences(
    response: Response,
):
    response.headers['X-Planner-Version'] = "1"

    response.delete_cookie(
        key="planer_view",
        path="/preferences",
    )

    response.status_code = status.HTTP_204_NO_CONTENT

    return response