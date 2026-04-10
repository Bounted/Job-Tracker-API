from fastapi import FastAPI
from routes import tasks, users
from auth import auth_router


app = FastAPI()
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth_router)
