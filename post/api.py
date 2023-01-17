from typing import List

from fastapi import APIRouter, Form, Depends
from starlette.templating import Jinja2Templates

from user.auth import get_current_user

from .schemas import GetListPost, UploadPost
from .models import Post, User
from .services import save_post, delete_post_service, update_post_service

post_router = APIRouter(prefix='/post', tags=["post"])
templates = Jinja2Templates(directory="templates")


@post_router.post("/", response_model=UploadPost)
async def create_post(
        title: str = Form(...),
        description: str = Form(...),
        user: User = Depends(get_current_user)
):
    """ Add post """
    return await save_post(title=title, description=description, user=user)


@post_router.put("/update/{pk}")
async def update_post(
        post_id: int = Form(...),
        title: str = Form(...),
        description: str = Form(...),
        user: User = Depends(get_current_user)
):
    """ Update post """
    return await update_post_service(post_id=post_id, title=title, description=description, user=user)


@post_router.delete("/delete/{pk}")
async def delete_post(
        post_id: int = Form(...),
        user: User = Depends(get_current_user)
):
    """ Delete post """
    return await delete_post_service(post_id=post_id, user_id=int(user[0]))


@post_router.get("/user/{user_name}", response_model=List[GetListPost])
async def get_list_post(user_name: str):
    return await Post.objects.filter(user__username=user_name).all()


@post_router.get("/index/{pk}")
async def get_post(post_pk: int):
    return await Post.objects.get(id=post_pk)


@post_router.post("/like/{pk}", status_code=201)
async def add_like(post_pk: int, user: User = Depends(get_current_user)):
    _post = await Post.objects.select_related("like_user").get(pk=post_pk)
    _user = await User.objects.get(id=int(user[0]))
    if _post.user != int(user[0]):
        if _user in _post.like_user:
            _post.like_count -= 1
            await _post.like_user.remove(_user)
        else:
            _post.like_count += 1
            await _post.like_user.add(_user)
    await _post.update()
    return _post.like_count


@post_router.post("/dislike/{pk}", status_code=201)
async def add_dislike(post_pk: int, user: User = Depends(get_current_user)):
    _post = await Post.objects.select_related("dislike_user").get(pk=post_pk)
    _user = await User.objects.get(id=int(user[0]))
    if _post.user != int(user[0]):
        if _user in _post.dislike_user:
            _post.like_count -= 1
            await _post.dislike_user.remove(_user)
        else:
            _post.like_count += 1
            await _post.dislike_user.add(_user)
    await _post.update()
    return _post.dislike_count
