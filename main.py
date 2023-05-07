from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routers import root, registration, login

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()

app.include_router(root.router)
app.include_router(registration.router)
app.include_router(login.router)
