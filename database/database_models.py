import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .db import db, metadata, sqlalchemy


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", UUID, index=True, primary_key=True, default=uuid.uuid4),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String)
)


class User:
    @classmethod
    async def get_by_id(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        await db.execute(query)
        created = await User.get_by_id(user["id"])
        return created
    
    @classmethod
    async def get_by_username(cls, username):
        query = users.select().where(users.c.username == username)
        user = await db.fetch_one(query)
        return user
    
    @classmethod
    async def get_by_email(cls, email):
        query = users.select().where(users.c.email == email)
        user = await db.fetch_one(query)
        return user
