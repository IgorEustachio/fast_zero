from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoPublic, TodoSchema
from fast_zero.security import get_current_user

T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Session = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema, session: T_Session, user: T_CurrentUser
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        status=todo.status,
        user_id=user.id,
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo
