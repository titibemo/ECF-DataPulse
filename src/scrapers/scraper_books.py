import re
import time
from typing import Optional, Generator
from urllib.parse import urljoin
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

from config.settings import scraper_books_config

logger = structlog.get_logger()


@dataclass
class Book:
    """Représentation d'un livre."""
    title: str
    price: str
    rating: str
    availability: str
    category: str

    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour MongoDB."""
        return {
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "availability": self.availability,
            "category": self.category
        }
    
class BooksScraper:
    def __init__(self):
        self.base_url = scraper_books_config.base_url
        self.delay = scraper_books_config.delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure la session HTTP."""
        self.session.headers.update({
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        })

    def scrape_complete(
        self,
        max_pages: int = None
    ) -> dict:
        """
        Scrape complet : livres (titre, prix, note, disponibilité, catégorie).
        
        Args:
            max_pages: Limite de pages
            
        Returns:
            {books: [...]}
        """
        books = []

        logger.info("scraping_started", max_pages=max_pages)
        
        for book in self.scrape_all_books(max_pages):
            books.append(book)
                    
        return {
            "books": books,
        }
    
    def scrape_all_books(
        self,
        max_pages: int = None
    ) -> Generator[Book, None, None]:
        """
        Scrape tous les livres avec pagination.
        
        Args:
            max_pages: Limite de pages (None = toutes)
            
        Yields:
            Objets Book
        """
        max_pages = max_pages or scraper_books_config.max_pages
        page = 1
        url = self.base_url
        
        while url and page <= max_pages:
            logger.info("scraping_page", page=page)
            
            soup = self._fetch_page(url)
            if not soup:
                break

            
            # Récupérer les liens vers les détails des livres
            links_details_books = soup.select(".product_pod h3 a[href]")
            if not links_details_books:
                break

            for details_book in links_details_books[:2]: #TODO ENLEVER [:2]
                details_book_url = urljoin(url, details_book["href"])

                soup_detail = self._fetch_page(details_book_url)
                if not soup_detail:
                    continue

                book = self._parse_book(soup_detail)
                if book:
                    yield book
            
            # Page suivante
            url = self._get_next_page(soup, url)
            page += 1

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page.
        
        Args:
            url: URL à récupérer
            
        Returns:
            BeautifulSoup ou None
        """
        try:
            logger.debug("fetching", url=url)
            response = self.session.get(url, timeout=scraper_books_config.timeout)

            response.raise_for_status()
            
            # Politesse
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, "lxml")
            
        except requests.RequestException as e:
            logger.error("fetch_failed", url=url, error=str(e))
            raise
    
    def _parse_book(self, div: str) -> Optional[Book]:
        title = div.select_one("h1").text.strip()
        price = div.select_one(".price_color").text.strip()
        rating = div.select_one("p.star-rating")["class"][1]
        #availability = div.select_one(".instock.availability").find_all(text=True)[-1].strip()
        availability = int(re.search(r'\d+', div.select_one(".instock.availability").find_all(text=True)[-1]).group())
        category = div.select("ul.breadcrumb li a")[2].text.strip()

        # Convertir le prix en euros
        price = self._change_currency(price)

        return Book(title=title, price=price, rating=rating, availability=availability, category=category)


    def _get_next_page(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Trouve l'URL de la page suivante."""
        next_li = soup.find("li", class_="next")

        if next_li:
            next_link = next_li.find("a", href=True)
            if next_link:
                logger.debug("next_page_found", url=next_link["href"])
                return urljoin(url, next_link["href"])
    
        
        logger.debug("next_page_not_found")
        return None
    
    def _change_currency(self, price: str) -> str:
        return price.replace("£", "€")
    
    def close(self) -> None:
        """Ferme la session."""
        self.session.close()