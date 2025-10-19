from database import get_connection
import asyncio



async def main():
    async with get_connection() as conn:
        await conn.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS product (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description VARCHAR(100),
            price INT,
            created_at  DATE DEFAULT CURRENT_DATE,
            user_id INT REFERENCES users(id) ON DELETE CASCADE
        )    
    """
    )
    print('Таблицы созданны!')



asyncio.run(main())