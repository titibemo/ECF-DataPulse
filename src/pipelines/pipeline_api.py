from config.settings import api_config
from src.extractor import Extractor
import structlog

logger = structlog.get_logger()
class APIPipeline:
    def __init__(self):
        self.api_extractor = Extractor()

    def run(self, city: str ="20 avenue de Segur Paris"):
        logger.info("fetching api")

        params = {
            "q": city,
            "limit": 2
        }

        data = self.api_extractor.extract_api("search/", params=params)

        print(data)

