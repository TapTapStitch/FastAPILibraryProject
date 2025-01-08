from fastapi import APIRouter, Depends
from ..crud.users import UsersCrud
from ..schemas.user import UserSchema, SignUpSchema, SignInSchema, UpdateUserSchema
from .shared.depends import get_users_crud

router = APIRouter()


@router.post("/sign-up", response_model=UserSchema, status_code=201)
async def sign_in(user: SignUpSchema, crud: UsersCrud = Depends(get_users_crud)):
    return crud.create(user)


@router.post("/sign-in", response_model=UserSchema)
async def sign_up(user: SignInSchema, crud: UsersCrud = Depends(get_users_crud)):
    return crud.get_user(user)


@router.patch("/{user_id}/update", response_model=UserSchema)
async def update_user(
    user_id: int, user: UpdateUserSchema, crud: UsersCrud = Depends(get_users_crud)
):
    return crud.update(user_id, user)
