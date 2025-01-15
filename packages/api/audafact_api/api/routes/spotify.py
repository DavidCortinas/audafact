from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List
import logging
from audafact_api.services.spotify import SpotifyClient
from audafact_api.config import settings

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

        if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
            raise HTTPException(
                status_code=500, detail="Spotify credentials not configured"
            )

        spotify_client = SpotifyClient(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )

        results = []

        for genre in genres:
            logger.info(f"Searching for genre: {genre}")
            query = f'genre:"{genre}"'
            search_results = await spotify_client.search(
                q=query, type=",".join(types), limit=limit
            )

            # Keep the original Spotify response structure for each genre
            genre_result = {
                "genre": genre,
                "artists": search_results.get("artists", {"items": [], "total": 0}),
                "playlists": search_results.get("playlists", {"items": [], "total": 0}),
            }
            results.append(genre_result)

            logger.info(
                f"Found {len(genre_result['artists']['items'])} artists and {len(genre_result['playlists']['items'])} playlists for genre {genre}"
            )

        return JSONResponse(content={"results": results})

    except Exception as e:
        logger.error(f"Error in search_spotify: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
