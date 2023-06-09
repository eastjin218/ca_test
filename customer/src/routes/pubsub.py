from typing import Union,Optional

from fastapi import APIRouter, WebSocket
import aioredis

from database.redis_db import RedisConnection

pubsub_router = APIRouter(
    tags=["PubSub"],
)

redis_con = RedisConnection()
redis = redis_con.connect()

async def sending_message(message: Union[bool, str]):
    channel = f"status_channel"
    messages = f"{message}"
    await redis.publish(channel, messages)
  

@pubsub_router.post("/endpoint/")
async def endpoint():
    # 상태 변경 로직
    stable = False
    await sending_message(stable)
    print("endpoint training!! process")
    # 상태 변경
    stable = True
    await sending_message(stable)

    return {"message": "Endpoint execution completed"}

@pubsub_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global redis
    redis = await aioredis.Redis.from_url(
        "redis://redis", max_connections=100, decode_responses=True
    )

    await websocket.accept()
    channel = f"status_channel"

    # Redis Pub/Sub 구독 시작
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    while True:
        # data = await websocket.receive_text()
        message = await pubsub.get_message()
        if not isinstance(message ,type(None)):
            await websocket.send_text(f"Message text was: {message}")