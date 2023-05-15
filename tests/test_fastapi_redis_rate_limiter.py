import os
import time

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastapi_redis_rate_limiter import RedisClient, RedisRateLimiterMiddleware

# Initialize the FastAPI app for testing
app = FastAPI()
app.add_middleware(
    RedisRateLimiterMiddleware,
    redis_client=RedisClient(host=os.environ.get("REDIS_HOST", "localhost")),
    limit=5,
    window=10,
)


@app.get("/")
async def index():
    return {"message": "Hello, world!"}


@pytest.fixture(scope="module")
def test_client():
    # Create a test client using the FastAPI app
    with TestClient(app) as client:
        yield client


def test_fastapi_rate_limit_not_exceeded(test_client):
    # Perform requests within the rate limit window
    time.sleep(5)
    for _ in range(3):
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, world!"}


def test_fastapi_rate_limit_exceeded(test_client):
    # Perform more than the allowed number of requests within the rate limit window
    for i in range(6):
        response = test_client.get("/")
        if i == 5:
            assert response.status_code == 429
            assert response.text == "Rate limit exceeded. Try again later."


def test_fastapi_rate_limit_reset(test_client):
    # Wait for the rate limit window to reset
    time.sleep(10)

    # Perform requests after the rate limit window has reset
    for _ in range(5):
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, world!"}
