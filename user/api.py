from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from .schemas import UserOut, UserAuth, TokenSchema, SystemUser
from .services import (
    create_access_token, save_user, get_user_login, create_refresh_token
)

from .auth import get_current_user

templates = Jinja2Templates(directory="templates")

user_router = APIRouter(tags=["auth"])


@user_router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@user_router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    new_user = await save_user(data.username, data.password)
    user_id = new_user.id
    user = {
        'id': str(user_id),
        'username': data.username

    }
    return user


@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_login(username=form_data.username, password=form_data.password)
    if user:
        return {
            "access_token": create_access_token(form_data.username),
            "refresh_token": create_refresh_token(form_data.username),
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )


@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    my_user = {'id': user[0],
               'username': user[1]
               }
    return my_user
