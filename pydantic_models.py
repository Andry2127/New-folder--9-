from typing import Optional

from pydantic import Field, BaseModel



class UserModelResponse(BaseModel):
    name: Optional[str] = Field(None, title="Users name")
    email: str = Field(...)




class UserModel(UserModelResponse):
    password: str = Field(...)





