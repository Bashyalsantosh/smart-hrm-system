from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models.user import User

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"