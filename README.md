[![Fastapi rate limiter](https://github.com/iunary/fastapi-redis-rate-limiter/actions/workflows/app.yml/badge.svg)](https://github.com/iunary/fastapi-redis-rate-limiter/actions/workflows/app.yml)
# Fastapi redis rate limiter middleware

Redis Rate Limiter Middleware is a Python module that provides rate limiting functionality for FastAPI applications using Redis as the storage backend. It allows you to limit the number of requests a client can make within a specified time window.

## Features

- Simple integration with FastAPI applications
- Customizable rate limit and time window
- Uses Redis as the storage backend for efficient rate limiting
- Easy to configure and use

## Installation

Install the Redis Rate Limiter Middleware module using `pip`:

```shell
pip install fastapi_redis_rate_limiter
```

## Usage

Here's an example of how to use the Redis Rate Limiter Middleware in a FastAPI application:

```python
from fastapi import FastAPI
from fastapi_redis_rate_limiter import RedisRateLimiterMiddleware, RedisClient

app = FastAPI()

# Initialize the Redis client
redis_client = RedisClient(host="localhost", port=6379, db=0)

# Apply the rate limiter middleware to the app
app.add_middleware(RedisRateLimiterMiddleware, redis_client=redis_client, limit=40, window=60)

@app.get("/limited")
async def limited():
    return {"message": "This is a protected endpoint."}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

In this example, we create a FastAPI application and initialize a Redis client using `RedisClient`. Then, we add `RedisRateLimiterMiddleware` to the app middleware using `add_middleware` and by passing in Redis client, rate limit, and time window.

Make sure to adjust the Redis connection parameters (host, port, and db) according to your Redis server configuration.

## Configuration

The RedisRateLimiterMiddleware accepts the following parameters:

- `app` (FastAPI): The FastAPI application instance.
- `redis_client` (RedisClient): The Redis client instance for interacting with Redis.
- `limit` (int): The maximum number of requests allowed within the time window.
- `window` (int): The time window in seconds within which the requests are limited (default: 60 seconds).

Adjust the `limit` and `window` values according to your desired rate limiting requirements.

## Contributions

Contributions, issues, and feature requests are welcome! Feel free to open a new issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.