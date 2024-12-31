from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
import tempfile
import os
from services.audio import (
    predict_tags_from_segments,
    predict_tags_from_file,
    predict_tags_from_qtrs
)
from services.downloader import download_audio_from_url
from core.config import settings

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


@router.get("/tags/url/quick")
async def get_quick_tags_by_url(
    url: str = Query(..., description="URL of the audio to analyze")
):
    audio_file_path = None
    try:
        logger.info(f"Processing URL for quick analysis: {url}")
        is_soundcloud = "soundcloud.com" in url
        logger.info(f"Source type: {'SoundCloud' if is_soundcloud else 'YouTube'}")

        audio_file_path = download_audio_from_url(url)
        logger.info(f"Audio downloaded successfully to: {audio_file_path}")

        predictions = predict_tags_from_qtrs(audio_file_path, settings.MODEL_PATH)
        logger.info(f"Quick tag predictions generated")

        response_data = {
            "predictions": predictions,
            "source": "soundcloud" if is_soundcloud else "youtube",
            "status": "success",
            "analysis_type": "quick"
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "source": "soundcloud" if "soundcloud.com" in url else "youtube",
                "status": "error",
                "analysis_type": "quick"
            }
        )
    finally:
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
                logger.info(f"Temporary file removed: {audio_file_path}")
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")


@router.post("/tags/file/quick")
async def get_quick_tags_by_file(
    file: UploadFile = File(..., max_size=10 * 1024 * 1024)
):
    audio_file_path = None
    try:
        logger.info(f"Received file for quick analysis: {file.filename}")
        logger.info(f"File content type: {file.content_type}")
        logger.info(f"File size: {file.size if hasattr(file, 'size') else 'unknown'}")

        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            content = await file.read()
            logger.info(f"Read file content size: {len(content)}")
            temp_audio.write(content)
            audio_file_path = temp_audio.name
            logger.info(f"Saved to temporary file: {audio_file_path}")

        # Get predictions using quarter segments method
        predictions = predict_tags_from_qtrs(audio_file_path, settings.MODEL_PATH)
        
        if not predictions:
            raise HTTPException(
                status_code=500,
                detail="No predictions generated"
            )

        # Return results
        return JSONResponse(
            content={
                "predictions": predictions,
                "status": "success",
                "analysis_type": "quick"
            }
        )

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
                logger.info(f"Temporary file removed: {audio_file_path}")
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")
