from sqlalchemy import select

from src.products.models import User


async def select_user_repository(db, username):
    result = await db.scalar(select(User).where(User.username == username))
    return result