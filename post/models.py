import datetime
import ormar
from typing import Optional, Union, Dict, List
from db import MainMata

from user.models import User


class UserLike(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)


class UserDisLike(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)


class Post(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user_post")
    like_count: int = ormar.Integer(default=0)
    like_user: Optional[Union[List[User], Dict]] = ormar.ManyToMany(
        User, related_name="like_users", through=UserLike
    )
    dislike_count: int = ormar.Integer(default=0)
    dislike_user: Optional[Union[List[User], Dict]] = ormar.ManyToMany(
        User, related_name="dislike_users", through=UserDisLike
    )
