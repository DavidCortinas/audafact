from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
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
) -> JSONResponse:
    audio_file_path = None
    try:
        logger.info(f"Starting analysis for URL: {url}")
        is_soundcloud = 'soundcloud.com' in url
        logger.info(f"Source type: {'SoundCloud' if is_soundcloud else 'YouTube'}")
        
        audio_file_path = download_audio_from_url(url)
        logger.info(f"Audio downloaded successfully to: {audio_file_path}")

        genre_predictions = predict_genre_from_segments(
            audio_file_path, settings.MODEL_PATH
        )
        logger.info(f"Genre predictions generated: {genre_predictions}")

        response_data: Dict[str, Any] = {
            "genres": genre_predictions,
            "source": "soundcloud" if is_soundcloud else "youtube",
            "status": "success"
        }
        
        logger.info("Sending successful response")
        return JSONResponse(
            content=response_data,
            status_code=200,
            headers={"X-Source-Type": "soundcloud" if is_soundcloud else "youtube"}
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "source": "soundcloud" if 'soundcloud.com' in url else "youtube",
                "status": "error"
            }
        )
    finally:
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
                logger.info(f"Temporary file removed: {audio_file_path}")
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")


# For file upload-based genre analysis
@router.post("/genres/file")
async def get_genres_by_file(file: UploadFile = File(..., max_size=10 * 1024 * 1024)):
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
