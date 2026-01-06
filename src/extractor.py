import requests
from config.settings import APIConfig
import pandas as pd

import structlog

import structlog
logger = structlog.get_logger()

class Extractor:
    def __init__(self):
        self.api_config = APIConfig()

    def extract_api(self, endpoint, params=None):
        """Extract data from API. Returns a pandas dataframe."""
        try:
            logger.info(f"Extraction de {self.api_config.base_url}{endpoint}")

            headers = {}

            if self.api_config.api_key:
                headers['Authorization'] = f'Bearer {self.api_config.api_key}'

            response = requests.get(
                f"{self.api_config.base_url}/{endpoint}",
                params=params,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            logger.info(f"Données extraites")

            return pd.DataFrame(data) if isinstance(data, list) else data

        except Exception as e:
            logger.error(f"Erreur extraction API: {e}")
            raise