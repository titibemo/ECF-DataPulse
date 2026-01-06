from src.extractor import Extractor
import structlog

logger = structlog.get_logger()
class APIPipeline:
    '''
    API Pipeline for geocoding data from adresse.data.gouv.fr.
    Will be used with Excel pipeline to geocode addresses from partenaire_librairies.xlsx
    '''
    def __init__(self):
        self.api_extractor = Extractor()

    def get_geocode(self, address: str):
        '''
        Get getcode from adress
        
        :param address (e.g: "1 rue de la paix 75001 Paris"):
        :type address: str
        '''
        logger.info("geocoding_address", address=address)

        try:
            params = {
                "q": address,
                "limit": 1
            }

            data = self.api_extractor.extract_api("search/", params=params)
            return data
        except Exception as e:
            logger.error("geocoding_failed", address=address, error=str(e))
            return None


