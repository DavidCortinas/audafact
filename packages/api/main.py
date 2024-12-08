import uvicorn
from audafact_api.core.config import settings

if __name__ == "__main__":
    port = int(settings.PORT)
    uvicorn.run(
        "audafact_api.api.app:app",
        host="0.0.0.0",
        port=port,
        reload=settings.ENV == "development",
    )
