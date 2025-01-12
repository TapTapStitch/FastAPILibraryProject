from fastapi import APIRouter, Depends, Response
from app.crud.users import UsersCrud
from app.schemas.user import UserSchema, SignUpSchema, SignInSchema, UpdateUserSchema
from app.routers.shared.depends import get_users_crud
from app.services.authorization import create_jwt_token, get_current_user
from app.schemas.token import Token
from app.routers.shared.response_templates import (
    bad_request_response,
    invalid_authentication_responses,
    invalid_password_response,
    not_found_response,
    combine_responses,
)

router = APIRouter()


@router.post(
    "/sign_up", status_code=201, responses=bad_request_response("Email already in use")
)
async def sign_up(user_data: SignUpSchema, crud: UsersCrud = Depends(get_users_crud)):
    crud.sign_up_user(user_data)
    return Response(status_code=201)


@router.post(
    "/sign_in",
    response_model=Token,
    responses=combine_responses(
        invalid_password_response(),
        not_found_response("User"),
    ),
)
async def sign_in(
    user_data: SignInSchema,
    crud: UsersCrud = Depends(get_users_crud),
):
    user = crud.sign_in_user(user_data)
    return create_jwt_token(user.id)


@router.get(
    "/current_user",
    response_model=UserSchema,
    responses=invalid_authentication_responses(),
)
async def show_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.patch(
    "/current_user",
    response_model=UserSchema,
    responses=combine_responses(
        invalid_authentication_responses(),
        bad_request_response("Email already in use"),
    ),
)
async def update_current_user(
    user_data: UpdateUserSchema,
    current_user=Depends(get_current_user),
    crud: UsersCrud = Depends(get_users_crud),
):
    return crud.update_user(current_user, user_data)


@router.delete(
    "/current_user", status_code=204, responses=invalid_authentication_responses()
)
async def delete_current_user(
    current_user=Depends(get_current_user),
    crud: UsersCrud = Depends(get_users_crud),
):
    crud.remove_user(current_user)
    return Response(status_code=204)
