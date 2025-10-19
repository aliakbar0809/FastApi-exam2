from database import get_connection
from fastapi import HTTPException
import asyncpg

# CRUD FROM USERS
async def create_user(username:str,email:str,password:str):
    async with get_connection()as conn:
        try:
            user_id = await conn.fetchval(
                "INSERT INTO users(username,email,password) VALUES($1,$2,$3) RETURNING id",
                username,email,password
            )
            return user_id
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Email должун быть уникальным, а такое email уже существует!"
            )
        


async def get_users():
    async with get_connection() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        return [dict(row) for row in rows]
    


async def get_user_by_id(id:int):
    async with get_connection() as conn:
        res = await conn.fetchrow("SELECT * FROM users WHERE id = $1",id)
        if res:
            return dict(res)
        return "Такого пользователя не существует"
    


async def update_user(id:int,username:str,email:str,password:str):
    async with get_connection() as conn:
        try:
            res = await conn.fecthrow(
                "UPDATE users SET username = $1, email = $2,password = $3 RETURNING id,username,email,password",
                username,email,password,id
            )
            if not res:
                raise HTTPException(status_code=404,detail="Пользователь не найден!")
            return dict(res)
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Email должен быть уникальным, а такой email уже существует!"
            )



async def delete_user(id:int):
    async with get_connection() as conn:
        res = await conn.execute("DELETE FROM users WHERE id = $1",id)
        if res == "DELETE 0":
            raise HTTPException(status_code=404, detail="Пользователь не найден!")
        return {"message": "Пользователь успешно удалён"}
    




# CRUD FROM PRODUCT

async def create_product(title: str, description: str, price: int, user_id: int):
    async with get_connection() as conn:
        try:
            product_id = await conn.fetchval(
                "INSERT INTO product(title, description, price, user_id) VALUES ($1, $2, $3, $4) RETURNING id",
                title, description, price, user_id
            )
            return product_id
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Ошибка: возможно, вы указали цену меньше 0 или не заполнили все поля."
            )
        

async def get_product():
    async with get_connection() as conn:
        rows = await conn.fetch("SELECT * FROM product")
        return [dict(row) for row in rows]
    

async def get_product_by_id(id: int):
    async with get_connection() as conn:
        res = await conn.fetchrow("SELECT * FROM product WHERE id = $1", id)
        if res:
            return dict(res)
        return None
    

async def update_product(id: int, title: str, description: str, price: int, user_id: int):
    async with get_connection() as conn:
        try:
            res = await conn.fetchrow(
                "UPDATE product SET title = $1, description = $2, price = $3, user_id = $4 WHERE id = $5 RETURNING *",
                title, description, price, user_id, id
            )
            if not res:
                raise HTTPException(status_code=404, detail="Продукт не найден!")
            return dict(res)
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Ошибка: возможно, цена меньше 0 или не все данные указаны."
            )
        


async def delete_product(id: int):
    async with get_connection() as conn:
        res = await conn.execute("DELETE FROM product WHERE id = $1", id)
        if res == "DELETE 0":
            raise HTTPException(status_code=404, detail="Продукт не найден!")
        return {"message": "Продукт успешно удалён"}