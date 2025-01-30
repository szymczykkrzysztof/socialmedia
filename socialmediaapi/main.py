from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from socialmediaapi.database import database
from socialmediaapi.routers.posts import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
