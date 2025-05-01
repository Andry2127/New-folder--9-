from typing import Optional, List, Union

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from fastapi.concurrency import asynccontextmanager
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
import uvicorn

from models import User, get_db,  database
from pydantic_models import UserModel, UserModelResponse


@asynccontextmanager
async def lifespan():
    await database.connect()
    yield
    await database.disconnect()
    


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")
app= FastAPI(lifespan=lifespan)


async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token != "1234":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ти гей???")
    
    user = db.query(User).where(User.id == 1).one()
    return user  

@app.post("/token/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "user" and form_data.password == "pass":
        return dict (access_token="1234", token_type="bearer")  
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong password or username")


@app.get("/users/me/", response_model=UserModelResponse)
async def get_user_me(current_user: User = Depends(get_user)):
    return current_user    


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def add_user(user_model: UserModel, db: Session = Depends(get_db)):
    user = User(**user_model.model_dump())
    db.add(user)
    db.commit()
  







if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)