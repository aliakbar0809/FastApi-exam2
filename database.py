import asyncpg
from contextlib import asynccontextmanager
import os



DB_CONFIG = {
    "host":"localhost",
    "port":5432,
    "database":"Exam2",
    "user":"postgres",
    "password":"softclub1122"
}




@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        await conn.close()
