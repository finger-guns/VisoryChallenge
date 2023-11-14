from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from .config import get_settings
from .event.router import router as event_router

settings = get_settings()


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

if settings.ENVIRONMENT_TYPE != "PRODUCTION":
    app.debug = True


origins = [

]


if settings.ENVIRONMENT_TYPE == "LOCAL":
    origins.append("*")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.redirect_slashes = False

base_router = APIRouter(
    prefix="/api",
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc):
    """
    Override default exception handler to return better exceptions for frontend
    """
    if exc.detail == "Wii Exception":
        error_detail = {
            "detail": {
                "user_message": exc.user_message,
                "message": exc.message,
            }
        }

    else:
        error_detail = {
            "detail": {
                "user_message": "Invalid request to server",
                "message": str(exc.detail),
            }
        }

    return JSONResponse(
        content=error_detail,
        status_code=exc.status_code,
    )


@app.get("/ping")
def handle_ping_pong() -> dict[str, str]:
    return {"ping": "pong"}


@app.get("/healthz", response_model=int)
def handle_healthz() -> int:
    return HTTP_200_OK

base_router.include_router(
    event_router,
    prefix="/event",
    tags=["event"],
)

app.include_router(
    base_router,
)
