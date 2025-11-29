from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import *


app = FastAPI(docs_url = "/api/users/docs" ,   
  openapi_url = "/api/users/openapi.json" )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/users/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
async def health():
    return {"status": "ok"}

app.include_router(UserRouter)