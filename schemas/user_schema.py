from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserRead(BaseModel):
    id: int
    email: str
    username: str

    model_config = ConfigDict(from_attributes=True)