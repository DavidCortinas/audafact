from setuptools import setup, find_packages

setup(
    name="audafact-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Core API packages
        "fastapi==0.115.6",
        "uvicorn==0.32.1",
        "starlette==0.41.3",
        "python-multipart==0.0.19",
        # ML and Audio Processing
        "essentia-tensorflow==2.1b6.dev1110",
        "tensorflow==2.12.1",
        "numpy==1.23.5",
        "scipy==1.10.1",
        # Audio Download
        "yt-dlp==2024.10.22",
        # Settings and Environment
        "pydantic==2.10.3",
        "pydantic-core==2.27.1",
        "pydantic-settings",
        "python-dotenv",
        # Utilities
        "requests==2.32.3",
        "PyYAML==6.0.2",
        "websockets==13.1",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "isort",
            "flake8",
            "mypy",
        ]
    },
    python_requires=">=3.8",
)
