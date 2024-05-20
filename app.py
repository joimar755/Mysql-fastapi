from fastapi import FastAPI  
from routes.products import product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

app.include_router(product)

