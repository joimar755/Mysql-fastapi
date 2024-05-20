from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from config.db import conn
from passlib.context import CryptContext
from models.db_p import products, user
from modelo.m_pro import producto 
from modelo.m_user import Users
import json

product = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@product.get("/products",response_model=List[producto])  
def getproduct():
    return conn.execute(products.select()).fetchall()

@product.post("/products",response_model=producto)  
def getnew(p: producto):
    new_products = {"name":p.name,"price":p.price,"stock":p.stock,"category_id":p.category_id}
    result = conn.execute(products.insert().values(new_products))
    conn.commit()
    return {**p.dict(), "id": result}


@product.get("/products/{id}",response_model=producto)  
def index(id:str):
    product = conn.execute(products.select().where(products.c.id == id)).first()
    if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

@product.delete("/products/{id}")  
def delete(id : str):
    product = conn.execute(products.delete().where(products.c.id == id))
    if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
    return product 

@product.put("/products/{id}",response_model=producto)  
def index(id:str, p: producto):
    new_products = {"name":p.name,"price":p.price,"stock":p.stock,"category_id":p.category_id}
    result = conn.execute(products.update().values(new_products).where(products.c.id == id))
    conn.commit()
    return conn.execute(products.select().where(products.c.id == id)).first() 

@product.post("/usuario",response_model=Users)  
def get_user(users:Users):
    new_users = {"username":users.username}
    new_users["password"] = pwd_context.hash(users.password.encode("utf-8"))
    result = conn.execute(user.insert().values(new_users)) 
    query = conn.execute(user.select().where(user.c.id == result.lastrowid)).first()
    conn.commit()
    return query


