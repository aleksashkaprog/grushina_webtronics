from fastapi import HTTPException
from starlette import status

from .models import Post, User
from .schemas import UploadPost, DeletePost


async def save_post(
        title: str,
        description: str,
        user: User
):
    UploadPost(title=title, description=description)
    return await Post.objects.create(user=user[0], title=title, description=description)


async def delete_post_service(
        post_id: int,
        user_id: int
):
    DeletePost(post_id=post_id, user_id=user_id)
    return await Post.objects.delete(id=post_id, user=user_id)


async def update_post_service(
        post_id: int,
        title: str,
        description: str,
        user: User
):
    _post = await Post.objects.get(id=post_id)
    if _post.user == int(user[0]):
        _post.title = title
        _post.description = description
        await _post.update()
        return _post
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

