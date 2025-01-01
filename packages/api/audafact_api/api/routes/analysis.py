from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
import asyncio
import os
from typing import Dict, Any
from ...services.downloader import download_audio_from_url
from ...services.audio import analyze_audio_quick

logger = logging.getLogger(__name__)
router = APIRouter()

async def cleanup_cached_file(file_path: str) -> None:
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")
    except Exception as e:
        logger.error(f"Error removing temporary file: {str(e)}")

@router.get("/analysis/url/quick")
async def get_quick_analysis_by_url(
    background_tasks: BackgroundTasks,
    url: str = Query(..., description="URL of the audio to analyze")
) -> Dict[str, Any]:
    """Get quick analysis of audio from URL."""
    try:
        logger.info(f"Starting quick analysis for URL: {url}")
        source_type = "soundcloud" if "soundcloud.com" in url else "youtube"
        logger.info(f"Source type: {source_type}")

        audio_file_path = await download_audio_from_url(url)
        logger.info(f"Audio downloaded successfully to: {audio_file_path}")
        
        # Add cleanup to background tasks
        background_tasks.add_task(cleanup_cached_file, audio_file_path)

        # Set a timeout for the analysis
        try:
            results = await asyncio.wait_for(
                analyze_audio_quick(audio_file_path),
                timeout=300  # 300 seconds timeout
            )
            
            return results  # Now returns the complete response object

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Analysis timed out"
            )

    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except asyncio.TimeoutError:
        logger.error("Analysis timed out")
        raise HTTPException(
            status_code=504,
            detail="Analysis timed out"
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            "error": str(e),
            "source": source_type,
            "status": "error",
            "analysis_type": "quick"
        }
