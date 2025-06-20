from fastapi import FastAPI
from app.routes import router
from security import get_password_hash

app = FastAPI()

app.include_router(router)

