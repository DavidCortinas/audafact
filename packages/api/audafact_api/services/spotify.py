import base64
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        if not client_id or not client_secret:
            raise ValueError("Both client_id and client_secret must be provided")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        
    async def get_token(self) -> str:
        if self.token:
            return self.token
            
        # Log credentials length (not the actual values)
        logger.info(f"Client ID length: {len(self.client_id)}")
        logger.info(f"Client Secret length: {len(self.client_secret)}")
            
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        try:
            # Log the request details (excluding sensitive info)
            logger.info(f"Making token request to: {url}")
            logger.info(f"Headers (excluding auth): {{'Content-Type': {headers['Content-Type']}}}")
            logger.info(f"Data: {data}")
            
            response = requests.post(url, headers=headers, data=data)
            
            # Log response details
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
                
            response.raise_for_status()
            json_result = response.json()
            
            if "access_token" not in json_result:
                logger.error(f"No access token in response: {json_result}")
                raise ValueError("No access token in Spotify response")
                
            self.token = json_result["access_token"]
            logger.info("Successfully obtained Spotify access token")
            return self.token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting Spotify token: {str(e)}")
            logger.error(f"Response content: {getattr(e.response, 'text', 'No response text')}")
            raise
        
    async def search(
        self, 
        q: str, 
        type: str,
        market: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        try:
            token = await self.get_token()
            logger.info(f"Searching Spotify with query: {q}, type: {type}")
            
            url = "https://api.spotify.com/v1/search"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            params = {
                "q": q,
                "type": type,
                "limit": limit,
                "offset": offset
            }
            if market:
                params["market"] = market
                
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            result = response.json()
            logger.info(f"Spotify search response: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Spotify: {str(e)}")
            raise
