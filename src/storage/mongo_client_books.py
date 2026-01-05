from datetime import datetime
from typing import Optional, Any
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import PyMongoError
import structlog

from config.settings import mongo_config

logger = structlog.get_logger()


class MongoDBStorageBooks:
    """
    Gestionnaire MongoDB pour les données structurées.
    
    Collections :
    - books :livre avec titre, prix, note (1-5 étoiles), disponibilité, catégorie
    - scraping_logs : Historique des exécutions
    """
    
    def __init__(self):
        self.client = MongoClient(mongo_config.connection_string)
        self.db = self.client[mongo_config.database]
        self.books = self.db["books"]
        self.scraping_logs = self.db["scraping_logs"]
        self._create_indexes()

    def _create_indexes(self):
        self.books.create_index("title", unique=True)

    ################## CREATE

    def insert_book(self, book: dict) -> None:
        """
        Insère ou met à jour un livre.
        
        Args:
            book: {title, rating,...}
            
        Returns:
            ID du document ou None
        """
        try:
            book["updated_at"] = datetime.utcnow()
            
            # Insert or update data
            result = self.books.update_one(
                {"title": book["title"], "price": book["price"] , "rating": book["rating"], "availability": book["availability"], "category": book["category"]},
                {"$set": book},
                upsert=True
            )
            
            if result.upserted_id:
                logger.debug("quote_inserted", author=book["author"])
                return str(result.upserted_id)
            
            return "updated"
            
        except PyMongoError as e:
            logger.error("quote_insert_failed", error=str(e))
            return None

    ################## LOGS

    def log_scraping_run(
        self,
        status: str,
        books_scraped: int,
        duration_seconds: float,
        errors: list = None
    ) -> None:
        """Enregistre un log de scraping."""
        self.scraping_logs.insert_one({
            "timestamp": datetime.utcnow(),
            "status": status,
            "books_scraped": books_scraped,
            "duration_seconds": duration_seconds,
            "errors": errors or []
        })

    def close(self) -> None:
        """Ferme la connexion."""
        self.client.close()