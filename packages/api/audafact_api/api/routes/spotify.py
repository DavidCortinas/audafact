from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List
import logging
from ...services.spotify import SpotifyClient
from ...core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/spotify/search")
async def search_spotify(
    genres: List[str] = Query(..., description="List of genres to search for"),
    types: List[str] = Query(["artist", "playlist"], description="Types to search for"),
    limit: int = Query(20, description="Number of results per type"),
):
    try:
        logger.info(f"Starting Spotify search with genres: {genres}, types: {types}")

        # Verify credentials are loaded
        if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
            raise HTTPException(
                status_code=500, detail="Spotify credentials not configured"
            )

        spotify_client = SpotifyClient(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )

        results = {
            "artists": {"items": [], "total": 0},
            "playlists": {"items": [], "total": 0},
        }

        for genre in genres:
            logger.info(f"Searching for genre: {genre}")
            query = f'genre:"{genre}"'  # Add quotes around genre
            search_results = await spotify_client.search(
                q=query,
                type=",".join(types),  # Join types with comma for single search
                limit=limit,
            )

            if "artists" in search_results:
                results["artists"]["items"].extend(search_results["artists"]["items"])
                results["artists"]["total"] = max(
                    results["artists"]["total"],
                    search_results["artists"].get("total", 0),
                )

            if "playlists" in search_results:
                results["playlists"]["items"].extend(
                    search_results["playlists"]["items"]
                )
                results["playlists"]["total"] = max(
                    results["playlists"]["total"],
                    search_results["playlists"].get("total", 0),
                )

        logger.info(
            f"Total results: {results['artists']['total']} artists, {results['playlists']['total']} playlists"
        )
        return JSONResponse(content=results)

    except Exception as e:
        logger.error(f"Error in search_spotify: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
