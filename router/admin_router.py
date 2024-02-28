from fastapi import APIRouter, Depends

from ..auth import auth

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.require_authorization)],
    responses={418: {"description": "I'm a teapot"}}
)


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
