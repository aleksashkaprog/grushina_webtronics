from pydantic import BaseModel


class UploadPost(BaseModel):
    title: str
    description: str


class DeletePost(BaseModel):
    post_id: int
    user_id: int


class GetListPost(BaseModel):
    id: int
    title: str
    description: str
    like_count: int
