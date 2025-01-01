import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
from ...services.audio import predict_mood_theme_from_audio
from ...services.downloader import download_audio_from_url
from ...core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/mood-themes/url")
async def get_mood_themes_by_url(
    url: str = Query(..., description="URL of the audio to analyze")
):
    try:
        audio_file_path = download_audio_from_url(url)
        predictions = await predict_mood_theme_from_audio(
            audio_file_path, settings.MODEL_PATH
        )
        return JSONResponse(content={"mood_themes": predictions})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mood-themes/file")
async def get_mood_themes_by_file(
    file: UploadFile = File(..., max_size=10 * 1024 * 1024)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            predictions = await predict_mood_theme_from_audio(
                temp_audio.name, settings.MODEL_PATH
            )
        return JSONResponse(content={"mood_themes": predictions})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
