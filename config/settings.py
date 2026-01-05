"""
Configuration centralisée du projet.
Utilise des variables d'environnement avec valeurs par défaut.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class MinIOConfig:
    endpoint: str = os.getenv("S3_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin123")
    secure: bool = os.getenv("S3_SECURE", "false").lower() == "true"
    bucket_images:str = "author-images"
    bucket_exports:str = "quotes-exports"
    bucket_backups:str = "quotes-backups"

@dataclass
class MongoDBConfig:
    host: str = os.getenv("MONGO_HOST", "localhost")
    port: int = int(os.getenv("MONGO_PORT", "27017"))
    username: str = os.getenv("MONGO_USER", "admin")
    password: str = os.getenv("MONGO_PASSWORD", "admin123")
    database: str = os.getenv("MONGO_DB", "scraping_db")

    @property
    def connection_string(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"

@dataclass
class ScraperBooksConfig:
    base_url:str = "https://books.toscrape.com"
    delay: float = 1.0 
    timeout: int = 30
    max_retries: int = 3
    max_pages: int = 20

@dataclass
class ScraperQuotesConfig:
    base_url:str = "https://quotes.toscrape.com"
    delay: float = 1.0 
    timeout: int = 30
    max_retries: int = 3
    max_pages: int = 20

@dataclass
class APIConfig:
    base_url: str = "https://api-adresse.data.gouv.fr/search/"
    #api_key: str = os.getenv("S3_SECRET_KEY", "minioadmin123")

@dataclass
class PostgresConfig:
    host: str = os.getenv("PG_HOST", "localhost")
    port: int = int(os.getenv("PG_PORT", "5432"))
    username: str = os.getenv("PG_USER", "postgres")
    password: str = os.getenv("PG_PASSWORD", "postgres123")
    database: str = os.getenv("PG_DB", "scraping_db")

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

minio_config = MinIOConfig()
mongo_config = MongoDBConfig()
scraper_books_config = ScraperBooksConfig()
scraper_quotes_config = ScraperQuotesConfig()
api_config = APIConfig()
postgres_config = PostgresConfig()


