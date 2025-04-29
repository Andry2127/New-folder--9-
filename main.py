from typing import Optional, List, Union

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from fastapi.concurrency import asynccontextmanager
from sqlalchemy import select, insert, update

from models import User, get_db,  database


@asynccontextmanager
async def lifespan():
    await database.connect()
    yield
    await database.disconnect()
    


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")
app= FastAPI(lifespan=lifespan)


async def get_user(token: str = Depends(oauth2_scheme)):
    if token != "1234":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ты гений, но не тот")
    return token    



        

