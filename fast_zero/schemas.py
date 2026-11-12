from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_zero.models import TodoStatus


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):  # schema out (schema de saída)
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):  # schema out (schema de saída)
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)


class TodoSchema(BaseModel):
    title: str
    description: str
    status: TodoStatus = Field(default=TodoStatus.todo)


class TodoPublic(TodoSchema):
    id: int
