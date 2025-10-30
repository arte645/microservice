from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
async def health():
    return {"status": "ok"}

app.include_router(UserRouter)
app.include_router(ArticleRouter)
app.include_router(CommentRouter)
