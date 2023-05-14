from setuptools import find_packages, setup

VERSION = "1.0.1"

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="fastapi_redis_rate_limiter",
    version=VERSION,
    description="fastapi rate limiter middleware",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yusuf",
    author_email="contact@yusuf.im",
    url="https://github.com/iunary/fastapi-redis-rate-limiter",
    license="MIT",
    install_requires=["fastapi", "redis", "starlette", "httpx"],
    keywords=["fastapi rate limiter", "redis", "middleware"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
