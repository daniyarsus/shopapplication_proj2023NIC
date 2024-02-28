from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from api.settings.config import PostgresDataBaseSettings, settings

async_engine = create_async_engine(
    #url=settings.pg_database.POSTGRES_DATABASE_URL,
    url="postgresql+asyncpg://postgres:5GbA2D6bDG66fBgE1bc-ed-C-GEfDgAC@viaduct.proxy.rlwy.net:50101/railway",
    echo=False
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    @property
    def pk(self):
        """Return the primary key value of the object"""
        return getattr(self, self.__mapper__.primary_key[0].name)

    def __repr__(self):
        return f'<{self.__class__.__name__}(id={self.pk})>'
