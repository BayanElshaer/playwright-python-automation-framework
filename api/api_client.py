import logging
import requests

logger = logging.getLogger(__name__)

class APIClient:
    """Simple API client for testing REST endpoints."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info("GET %s with params %s", url, params)
        response = requests.get(url, params=params)
        logger.debug("Response status: %s", response.status_code)
        return response

    def post(self, endpoint: str, data: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info("POST %s with data %s", url, data)
        response = requests.post(url, json=data)
        logger.debug("Response status: %s", response.status_code)
        return response
    
    def put(self, endpoint: str, data: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info("PUT %s with data %s", url, data)
        response = requests.put(url, json=data)
        logger.debug("Response status: %s", response.status_code)
        return response
    
    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info("DELETE %s", url)
        response = requests.delete(url)
        logger.debug("Response status: %s", response.status_code)
        return response