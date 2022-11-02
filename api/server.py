from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.router import router
from api.router.health import health_router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging, LimiterInit
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
)
from core.helpers.cache import Cache, RedisBackend, CustomKeyMaker
from core.helpers.redis import redis


def _init_routers(app_: FastAPI) -> None:
    app_.include_router(health_router)
    app_.include_router(router)


def _init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    @app_.on_event("startup")
    async def startup():
        await LimiterInit.init(redis)

    @app_.on_event("shutdown")
    async def startup():
        await LimiterInit.close()


def _on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def _generate_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=_on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def _init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="CICADA",
        description="CICADA API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=_generate_middleware(),
    )
    _init_routers(app_=app_)
    _init_listeners(app_=app_)
    _init_cache()
    return app_


app = create_app()
