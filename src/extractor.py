import logging
import requests
from config.settings import APIConfig
import pandas as pd

from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

import structlog
logger = structlog.get_logger()

class Extractor:
    def __init__(self):
        self.api_config = APIConfig()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def extract_api(self, endpoint, params=None):
        """Extrait données d'une API"""
        try:
            logger.info(f"Extraction de {self.api_config.base_url}{endpoint}")

            headers = {}
            # Si une clé d'API est fournie, on l'ajoute en header Authorization
            if self.api_config.api_key:
                headers['Authorization'] = f'Bearer {self.api_config.api_key}'

            # Appel HTTP GET
            response = requests.get(
                f"{self.api_config.base_url}/{endpoint}",
                params=params,
                headers=headers,
                timeout=30
            )
            # Lève une erreur si status code 4xx/5xx
            response.raise_for_status()

            data = response.json()

            logger.info(f"Données extraites")

            # Si l'API renvoie une liste, on la convertit en DataFrame
            return pd.DataFrame(data) if isinstance(data, list) else data

        except Exception as e:
            self.logger.error(f"Erreur extraction API: {e}")
            raise