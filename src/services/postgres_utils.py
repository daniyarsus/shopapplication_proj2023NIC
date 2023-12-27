import asyncpg

from src.settings.config import DATABASE_URL


postgres_conn = None


async def init_postgres():
    global postgres_conn
    postgres_conn = await asyncpg.connect(DATABASE_URL)
    print("PostgreSQL connection has been initialized")


async def close_postgres():
    global postgres_conn
    if postgres_conn:
        await postgres_conn.close()
        print("PostgreSQL connection has been closed")

