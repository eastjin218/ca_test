from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from database.connection import Settings

from routes.users import user_router
from routes.pubsub import pubsub_router
import uvicorn

import asyncio
import aioredis

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
app.include_router(pubsub_router,  prefix="/pubsub")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://172.30.1.169:8000/pubsub/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
check_status = "true"

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

@app.get("/health_check", tags=["root"])
async def health_check() -> dict:
    return {"message": "Welcome to LG Checklist tool!!_ca"}


if __name__=='__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)