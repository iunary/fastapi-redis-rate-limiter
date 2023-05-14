import time
from datetime import timedelta
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import PlainTextResponse
from typing import Union
from .redis_client import RedisClient


class RedisRateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting based on Redis.
    """

    def __init__(
        self,
        app,
        redis_client: RedisClient,
        limit: int,
        window: Union[int, timedelta] = timedelta(minutes=1),
    ):
        """
        Initializes the rate limiter middleware.

        Args:
            app (FastAPI): The FastAPI application.
            redis_client (RedisClient): The Redis client instance.
            limit (int): The maximum number of requests allowed within the window.
            window (int): The time window in seconds.
        """
        super().__init__(app)
        self.redis_client = redis_client
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Handles the incoming request and applies rate limiting.

        Args:
            request (Request): The incoming request.
            call_next (callable): The callable for invoking the next middleware or application.

        Returns:
            Response: The response generated by the application or an error response if the rate limit is exceeded.
        """
        # Retrieve the client's IP address or any other identifier
        client_ip = request.client.host

        # Create the Redis key using the client's IP and the current minute timestamp
        key = f"{client_ip}:{int(time.time() // self.window)}"

        # Check the current request count for the client
        request_count = self.redis_client.incr(key)
        if request_count is None:
            # Handle Redis error
            return PlainTextResponse("Internal server error.", status_code=500)

        if request_count == 1:
            # Set an expiration for the key if it's the first request within the window
            self.redis_client.expire(key, self.window)

        # Check if the client has exceeded the rate limit
        if request_count > self.limit:
            return PlainTextResponse(
                "Rate limit exceeded. Try again later.", status_code=429
            )

        response = await call_next(request)
        return response
