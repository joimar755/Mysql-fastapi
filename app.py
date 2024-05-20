from fastapi import FastAPI  
from routes.products import product

app = FastAPI() 

app.include_router(product)

