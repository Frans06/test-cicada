# Code copied from Fast-Limiter in order to make it work for our case

from math import ceil
from typing import Callable, Union, Optional

from pydantic import conint
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.websockets import WebSocket


class RateLimiter:
    def __init__(
        self,
        times: conint(ge=0) = 1000,
        milliseconds: conint(ge=-1) = 0,
        seconds: conint(ge=-1) = 0,
        minutes: conint(ge=-1) = 1,
        hours: conint(ge=-1) = 0,
        identifier: Optional[Callable] = None,
        callback: Optional[Callable] = None,
    ):
        self.times = times
        self.milliseconds = (
            milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        )
        self.identifier = identifier
        self.callback = callback

    async def _check(self, key):
        redis = LimiterInit.redis
        pexpire = await redis.evalsha(
            LimiterInit.lua_sha, 1, key, str(self.times), str(self.milliseconds)
        )
        return pexpire

    async def __call__(self, request: Request, response: Response):
        if not LimiterInit.redis:
            raise Exception(
                "You must call LimiterInit.init in startup event of fastapi!"
            )
        index = 0
        for route in request.app.routes:
            if route.path == request.scope["path"]:
                for idx, dependency in enumerate(route.dependencies):
                    if self is dependency.dependency:
                        index = idx
                        break

        # moved here because constructor run before app startup
        identifier = self.identifier or LimiterInit.identifier
        callback = self.callback or LimiterInit.http_callback
        rate_key = await identifier(request)
        key = f"{LimiterInit.prefix}:{rate_key}:{index}"
        pexpire = await self._check(key)
        if pexpire != 0:
            return await callback(request, response, pexpire)


class LimiterInit:
    redis = None
    prefix: str = None
    lua_sha: str = None
    identifier: Callable = None
    http_callback: Callable = None
    ws_callback: Callable = None
    lua_script = """local key = KEYS[1]
local limit = tonumber(ARGV[1])
local expire_time = ARGV[2]
local current = tonumber(redis.call('get', key) or "0")
if current > 0 then
 if current + 1 > limit then
 return redis.call("PTTL",key)
 else
        redis.call("INCR", key)
 return 0
 end
else
    redis.call("SET", key, 1,"px",expire_time)
 return 0
end"""

    @classmethod
    async def init(
        cls,
        redis,
        prefix: str = "fastapi-limiter",
    ):
        cls.redis = redis
        cls.prefix = prefix
        cls.identifier = default_identifier
        cls.http_callback = http_default_callback
        cls.ws_callback = ws_default_callback
        cls.lua_sha = await redis.script_load(cls.lua_script)

    @classmethod
    async def close(cls):
        await cls.redis.close()


async def default_identifier(request: Union[Request, WebSocket]):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host
    return ip + ":" + request.scope["path"]


async def http_default_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        HTTP_429_TOO_MANY_REQUESTS,
        "Too Many Requests",
        headers={"Retry-After": str(expire)},
    )


async def ws_default_callback(ws: WebSocket, pexpire: int):
    """
    default callback when too many requests
    :param ws:
    :param pexpire: The remaining milliseconds
    :return:
    """
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        HTTP_429_TOO_MANY_REQUESTS,
        "Too Many Requests",
        headers={"Retry-After": str(expire)},
    )
