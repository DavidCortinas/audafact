from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import logging
import os
import tempfile
from ...services.audio import predict_genre_from_segments
from ...services.downloader import download_audio_from_url
from ...core.config import settings
logger = logging.getLogger(__name__)
router = APIRouter()


class URLInput(BaseModel):
    url: str


# For URL-based genre analysis
@router.get("/genres/url")
async def get_genres_by_url(
    url: str = Query(..., description="URL of the audio to analyze")
):
    try:
        print(f"Processing URL: {url}")
        audio_file_path = download_audio_from_url(url)

        genre_predictions = predict_genre_from_segments(
            audio_file_path, settings.MODEL_PATH
        )
        return JSONResponse(content={"genres": genre_predictions})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if (
            "audio_file_path" in locals()
            and audio_file_path
            and os.path.exists(audio_file_path)
        ):
            try:
                os.remove(audio_file_path)
            except Exception as e:
                print(f"Error removing temporary file: {str(e)}")


# For file upload-based genre analysis
@router.post("/genres/file")
async def get_genres_by_file(
    file: UploadFile = File(..., max_size=10 * 1024 * 1024)
):
    try:
        logger.info(f"Received file: {file.filename}")
        logger.info(f"File content type: {file.content_type}")
        logger.info(f"File size: {file.size if hasattr(file, 'size') else 'unknown'}")

        print("Processing uploaded file")
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            content = await file.read()
            logger.info(f"Read file content size: {len(content)}")
            temp_audio.write(content)
            audio_file_path = temp_audio.name
            logger.info(f"Saved to temporary file: {audio_file_path}")

        genre_predictions = predict_genre_from_segments(
            audio_file_path, settings.MODEL_PATH
        )
        return JSONResponse(content={"genres": genre_predictions})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
