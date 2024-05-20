from typing import Optional
from pydantic import BaseModel

class Users(BaseModel):
    username:  str | None = None
    password:  str | None = None
    
    