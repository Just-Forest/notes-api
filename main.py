import uvicorn
from fastapi import FastAPI

from src.api.router import api_router

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
