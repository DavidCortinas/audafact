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
    limit: int = Query(20, description="Number of results per type")
):
    try:
        logger.info(f"Starting Spotify search with genres: {genres}, types: {types}")
        
        # Verify credentials are loaded
        if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
            raise HTTPException(
                status_code=500,
                detail="Spotify credentials not configured"
            )
        
        spotify_client = SpotifyClient(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET
        )
        
        results = {
            "artists": [],
            "playlists": []
        }
        
        for genre in genres:
            if "artist" in types:
                logger.info(f"Searching for artists with genre: {genre}")
                query = f"genre:\"{genre}\""  # Add quotes around genre
                artist_results = await spotify_client.search(
                    q=query,
                    type="artist",
                    limit=limit
                )
                
                if "artists" in artist_results and "items" in artist_results["artists"]:
                    results["artists"].extend(artist_results["artists"]["items"])
                    logger.info(f"Found {len(artist_results['artists']['items'])} artists for genre {genre}")
                else:
                    logger.warning(f"No artist results for genre {genre}")
                
            if "playlist" in types:
                logger.info(f"Searching for playlists with genre: {genre}")
                playlist_results = await spotify_client.search(
                    q=genre,
                    type="playlist",
                    limit=limit
                )
                
                if "playlists" in playlist_results and "items" in playlist_results["playlists"]:
                    results["playlists"].extend(playlist_results["playlists"]["items"])
                    logger.info(f"Found {len(playlist_results['playlists']['items'])} playlists for genre {genre}")
                else:
                    logger.warning(f"No playlist results for genre {genre}")
        
        logger.info(f"Total results: {len(results['artists'])} artists, {len(results['playlists'])} playlists")
        return JSONResponse(content=results)
        
    except Exception as e:
        logger.error(f"Error in search_spotify: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
