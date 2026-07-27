import uvicorn
from fastapi import FastAPI
from src.api.endpoints.system.authors import router
from src.api.endpoints.system import system_router
from src.api.endpoints.system.health import health_router
from src.database import engine, Base

Base.metadata.create_all(engine)
app = FastAPI()
for router in router, system_router, health_router:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
