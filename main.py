import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.router import api_router
from src.services.exceptions import AlreadyExists, InvalidCredentials, NotFound

app = FastAPI()
app.include_router(api_router)


@app.exception_handler(NotFound)
def handle_not_found(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AlreadyExists)
def handle_already_exists(request, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentials)
def handle_invalid_credentials(request, exc):
    return JSONResponse(
        status_code=401, content={"detail": "Incorrect name or password"}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
