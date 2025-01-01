import tempfile
import os
from ..shared.constants.headers import ROTATING_USER_AGENTS
import yt_dlp
import logging
from fastapi import HTTPException
import random
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)


def get_rotating_headers():
    return {
        "User-Agent": random.choice(ROTATING_USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.youtube.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }


@lru_cache(maxsize=32)
def get_cached_audio_path(url: str) -> str:
    """Cache the downloaded audio file path based on URL hash"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f"/tmp/audio_cache_{url_hash}.wav"


async def download_audio_from_url(url: str) -> str:
    cached_path = get_cached_audio_path(url)
    if os.path.exists(cached_path):
        return cached_path
        
    try:
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, "downloaded_audio.wav")
        logger.info(f"Temporary file path: {temp_audio_path}")

        ydl_opts = {
            "format": "bestaudio[ext=m4a]/best",
            "outtmpl": temp_audio_path,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "verbose": True,
            "http_headers": get_rotating_headers(),
            # Add cookies file if available
            # "cookiefile":
            # "cookies.txt" if os.path.exists("cookies.txt") else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.download([url])
                if result != 0:
                    raise HTTPException(
                        status_code=500, detail="Failed to download audio from URL"
                    )
            except yt_dlp.utils.DownloadError as e:
                error_message = str(e)
                if "Sign in to confirm you're not a bot" in error_message:
                    raise HTTPException(
                        status_code=429,
                        detail="YouTube rate limit detected. Please try again later or use a different URL.",
                    )
                elif "Video unavailable" in error_message:
                    raise HTTPException(
                        status_code=404, detail="Video not found or is unavailable"
                    )
                else:
                    logger.error(f"YouTube download error: {error_message}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"YouTube download failed: {error_message}",
                    )

        final_audio_path = f"{temp_audio_path}.wav"
        if not os.path.exists(final_audio_path):
            raise HTTPException(
                status_code=500, detail="Failed to save downloaded audio"
            )

        return final_audio_path

    except Exception as e:
        logger.error(f"Error during audio download: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail=f"Failed to download audio: {str(e)}"
        )
