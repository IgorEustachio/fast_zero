from sqlalchemy.ext.asyncio import (  # ext de extension
    AsyncSession,
    create_async_engine,
)

from fast_zero.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


# esse pragma é pro pytest ignorar a função
async def get_session():  # pragma: no cover
    # expire_on_commit: dados continuam guardados mesmo após commit
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
