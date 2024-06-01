from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from models import Claim
from database import engine, init_db
from api.endpoints import claims

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(claims.router)
