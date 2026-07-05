from pydantic import BaseModel, EmailStr


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


class UserDB(UserSchema):
    id: int
