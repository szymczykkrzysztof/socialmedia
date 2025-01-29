import uvicorn
from fastapi import FastAPI

from socialmediaapi.routers.post import router as post_router

app = FastAPI()
app.include_router(post_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
