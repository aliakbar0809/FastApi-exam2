from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from queries import *


# CRUD main.py for users
app = FastAPI(title="Users and Products CRUD", description="API для CRUD", version="1.0.0")

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    password:str


@app.get("/user{user_id}",response_model=dict,summary="Напишите id который вы хотите увидеть!")
async def get_user_endpoint(user_id:int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404,detail="Пользователь не найден!")
    return user




@app.post("/c_users",response_model=UserResponse,summary="Создайте нового пользователя!")
async def create_users_endpoint(user:UserCreate):
    user_id = await create_user(user.username,user.email,user.password)
    return UserResponse(id=user_id,username=user.username,email=user.email,password=user.password)




@app.get('/l_users',response_model=list[dict],summary="Вот все пользователи")
async def list_users_endpoint():
    users = await get_users()
    return users





@app.put("/user_update/{user_id}", response_model=UserResponse, summary="Обновить данные пользователя")
async def update_user_endpoint(user_id: int, user: UserCreate):
    updated_user = await update_user(user_id, user.username, user.email,user.password)
    return updated_user



@app.delete("/user_delete/{user_id}", summary="Удалить пользователя по ID")
async def delete_user_endpoint(user_id: int):
    result = await delete_user(user_id)
    return result




# CRUD for product


class ProductCreate(BaseModel):
    title: str
    description: str
    price: int
    user_id: int


class ProductResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    user_id: int



@app.get("/product{product_id}", response_model=dict, summary="Введите ID продукта, который хотите увидеть!")
async def get_product_endpoint(product_id: int):
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден!")
    return product


@app.post("/c_product", response_model=ProductResponse, summary="Создайте новый продукт!")
async def create_product_endpoint(product: ProductCreate):
    product_id = await create_product(product.title, product.description, product.price, product.user_id)
    return ProductResponse(
        id=product_id,
        title=product.title,
        description=product.description,
        price=product.price,
        user_id=product.user_id
    )


@app.get('/l_products', response_model=list[dict], summary="Вот все продукты")
async def list_products_endpoint():
    products = await get_product()
    return products


@app.put("/product_update/{product_id}", response_model=ProductResponse, summary="Обновить данные продукта")
async def update_product_endpoint(product_id: int, product: ProductCreate):
    updated_product = await update_product(
        product_id,
        product.title,
        product.description,
        product.price,
        product.user_id
    )
    return updated_product


@app.delete("/product_delete/{product_id}", summary="Удалить продукт по ID")
async def delete_product_endpoint(product_id: int):
    result = await delete_product(product_id)
    return result