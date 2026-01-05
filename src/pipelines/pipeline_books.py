from datetime import datetime
from typing import Optional
import pandas as pd
from tqdm import tqdm
import structlog

from src import BooksScraper, Book
from src.storage import MinIOStorage, MongoDBStorageBooks

logger = structlog.get_logger()


class BooksPipeline:
    """
    Pipeline ETL pour les livres.
    
    Workflow :
    1. Extract : Scraping des livres
    2. Transform : Nettoyage et enrichissement des données
    3. Load : Stockage MongoDB + exports MinIO
    """
        
    def __init__(self):
        self.scraper = BooksScraper()
        self.minio = MinIOStorage()
        self.mongodb = MongoDBStorageBooks()
        self.stats = {
            "books_scraped": 0,
            "errors": []
        }
    
    def process_book(self, book: Book) -> Optional[dict]:
        """Traite et stocke un livre."""
        try:
            book_data = book.to_dict()
            self.mongodb.insert_book(book_data)
            self.stats["books_scraped"] += 1
            return book_data
        except Exception as e:
            self.stats["errors"].append(str(e))
            return None

    def run(self, max_pages: int = 3, show_progress: bool = True):
        """
        Exécute le pipeline complet.
        
        Args:
            max_pages: Nombre max de pages
            show_progress: Afficher la progression
            
        Returns:
            Statistiques d'exécution
        """
        start_time = datetime.utcnow()
        logger.info("pipeline_started", max_pages=max_pages)

        try:

            data = self.scraper.scrape_complete(
                    max_pages=max_pages
                )
            
            # Traiter les livres
            books = data["books"]
            iterator = tqdm(books, desc="Processing books") if show_progress else books
            for book in iterator:
                self.process_book(book)
                
            end_time = datetime.utcnow()
            duration = end_time - start_time

            # Log du run
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.mongodb.log_scraping_run(
                status="success",
                books_scraped=self.stats["books_scraped"],
                duration_seconds=duration,
                errors=self.stats["errors"]
            )
        
        except Exception as e:
            logger.error("pipeline_failed", error=str(e))
            self.mongodb.log_scraping_run(
                status="failed",
                quotes_scraped=self.stats["quotes_scraped"],
                authors_scraped=self.stats["authors_scraped"],
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                errors=[str(e)]
            )
        
        finally:
            end_time = datetime.utcnow()
            self.stats["duration_seconds"] = (end_time - start_time).total_seconds()
            self.stats["start_time"] = start_time.isoformat()
            self.stats["end_time"] = end_time.isoformat()
        
        logger.info("pipeline_completed", stats=self.stats)
        return self.stats


    def close(self) -> None:
        """Ferme les connexions."""
        self.scraper.close()
        self.mongodb.close()
    
