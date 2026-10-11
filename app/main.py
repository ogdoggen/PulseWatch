from fastapi import FastAPI

from app.config import settings


app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/health/live", tags=["health"])
async def health_live() -> dict[str, str]:
    return {"status": "ok"}