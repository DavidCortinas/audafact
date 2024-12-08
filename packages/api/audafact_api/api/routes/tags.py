from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
import tempfile
import os
from ...services.audio import predict_tags_from_segments, predict_tags_from_file
from ...services.downloader import download_audio_from_url
from ...core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/tags/url")
async def get_tags_by_url(
    url: str = Query(..., description="URL of the audio to analyze")
):
    try:
        logger.info(f"Processing URL: {url}")
        audio_file_path = download_audio_from_url(url)
        predictions = predict_tags_from_file(audio_file_path, settings.MODEL_PATH)
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
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
                logger.error(f"Error removing temp file: {str(e)}")


@router.post("/tags/file")
async def get_tags_by_file(file: UploadFile = File(..., max_size=10 * 1024 * 1024)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            audio_file_path = temp_audio.name

            # Get predictions using both methods
            segmented_predictions = predict_tags_from_segments(
                audio_file_path, settings.MODEL_PATH
            )
            full_file_predictions = predict_tags_from_file(
                audio_file_path, settings.MODEL_PATH
            )

            return JSONResponse(
                content={
                    "segmented": segmented_predictions,
                    "full_file": full_file_predictions,
                }
            )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if "audio_file_path" in locals() and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
            except Exception as e:
                logger.error(f"Error removing temp file: {str(e)}")
