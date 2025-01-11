from fastapi import APIRouter, Depends, Response
from ..crud.users import UsersCrud
from ..schemas.user import UserSchema, SignUpSchema, SignInSchema, UpdateUserSchema
from .shared.depends import get_users_crud
from ..services.authorization import create_jwt_token, get_current_user_id
from ..schemas.token import Token

router = APIRouter()


@router.post("/sign_up", status_code=201)
async def sign_up(user_data: SignUpSchema, crud: UsersCrud = Depends(get_users_crud)):
    crud.create_user(user_data)
    return Response(status_code=201)


@router.post("/sign_in", response_model=Token)
async def sign_in(
    user_data: SignInSchema,
    crud: UsersCrud = Depends(get_users_crud),
):
    user = crud.get_user(user_data)
    return create_jwt_token(user.id)


@router.get("/current_user", response_model=UserSchema)
async def show_current_user(
    user_id: int = Depends(get_current_user_id),
    crud: UsersCrud = Depends(get_users_crud),
):
    return crud.get_user_by_id(user_id)


@router.patch("/current_user", response_model=UserSchema)
async def update_current_user(
    user_data: UpdateUserSchema,
    user_id: int = Depends(get_current_user_id),
    crud: UsersCrud = Depends(get_users_crud),
):
    return crud.update_user(user_id, user_data)


@router.delete("/current_user", status_code=204)
async def delete_current_user(
    user_id: int = Depends(get_current_user_id),
    crud: UsersCrud = Depends(get_users_crud),
):
    crud.remove_user(user_id)
    return Response(status_code=204)
