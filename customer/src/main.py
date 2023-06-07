from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from database.connection import Settings

from routes.users import user_router

import uvicorn

app = FastAPI()

settings = Settings()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router,  prefix="/user")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

@app.get("/health_check", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to LG Checklist tool!!_ca"}

if __name__=='__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)