# """Pipeline de données pour les citations."""

# from datetime import datetime
# from typing import Optional
# import pandas as pd
# from tqdm import tqdm
# #import structlog

# from src import QuotesScraper, Quote
# from src.storage import MinIOStorage, MongoDBStorage

# from utils.logger import setup_logging
# from utils.cli_args import get_cli_args

# import logging


# class QuotesPipeline:
#     """
#     Pipeline ETL pour les Produits ecommerce.
    
#     Workflow :
#     1. Extract : Scraping des citations et auteurs
#     2. Transform : Nettoyage et enrichissement
#     3. Load : Stockage MongoDB + exports MinIO
#     """
    
#     def __init__(self):
#         self.logger = logging.getLogger(__name__)
#         self.scraper = QuotesScraper()
#         self.minio = MinIOStorage()
#         self.mongodb = MongoDBStorage()
#         self.stats = {
#             "quotes_scraped": 0,
#             "errors": []
#         }

        
#     def run(
#         self,
#         max_pages: int = 1,
#         show_progress: bool = True
#     ) -> dict:
#         """
#         Exécute le pipeline complet.
        
#         Args:
#             max_pages: Nombre max de pages
#             show_progress: Afficher la progression
            
#         Returns:
#             Statistiques d'exécution
#         """
#         start_time = datetime.now()
#         self.logger.info(f"pipeline_started - max_pages={max_pages}")
        
#         try:
#             #delete all data
#             #self.mongodb.delete_all()

#             # Scrape complet
#             data: dict[str, list[Quote]] = self.scraper.scrape_complete(
#                 max_pages=max_pages,
#             )
            
#             # Ajouter les produits
#             quotes: list[Quote] = data["quotes"]
#             iterator = tqdm(quotes, desc="Processing quotes") if show_progress else quotes
            
#             for quote in iterator:
#                 self.process_quote(quote)

#             # Log du run
#             duration = (datetime.now() - start_time).total_seconds()
#             self.mongodb.log_scraping_run(
#                 status="success",
#                 quotes_scraped=self.stats["quotes_scraped"],
#                 duration_seconds=duration,
#                 errors=self.stats["errors"]
#             )
            
            
    
#         except Exception as e:
#             self.logger.error(f"pipeline_failed, , error={str(e)}")
#             self.mongodb.log_scraping_run(
#                 status="failed",
#                 quotes_scraped=self.stats["quotes_scraped"],
#                 duration_seconds=(datetime.now() - start_time).total_seconds(),
#                 errors=[str(e)]
#             )
        
#         finally:
#             end_time = datetime.now()
#             self.stats["duration_seconds"] = (end_time - start_time).total_seconds()
#             self.stats["start_time"] = start_time.isoformat()
#             self.stats["end_time"] = end_time.isoformat()

#         self.logger.info(f"======= pipeline_completed stats={self.stats}")
#         return self.stats
    

#     ################# LOAD
#     def process_quote(self, quote: Quote) -> Optional[dict]:
#         """Traite et stocke un produit."""
#         try:
#             quote_data = quote.to_dict()
#             self.mongodb.insert_quote(quote_data)
#             self.stats["quotes_scraped"] += 1
#             return quote_data
#         except Exception as e:
#             self.stats["errors"].append(str(e))
#             return None

#     ################### EXPORT
    
#     def export_csv(self, filepath: str = None) -> Optional[str]:
#         """
#         Exporte les citations en CSV.
        
#         Args:
#             filepath: Chemin local (optionnel)
            
#         Returns:
#             URI MinIO
#         """
#         quotes = self.mongodb.find_quotes(limit=10000)
        
#         if not quotes:
#             return None
        
#         # Convertir en DataFrame
#         df = pd.DataFrame(quotes)
        
#         # Nettoyer
#         if "_id" in df.columns:
#             df["_id"] = df["_id"].astype(str)
        
#         # Convertir les tags en string
#         if "tags" in df.columns:
#             df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if x else "")
        
#         # Sauvegarder localement
#         if filepath:
#             df.to_csv(filepath, index=False)
        
#         # Upload vers MinIO
#         csv_content = df.to_csv(index=False)
#         timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
#         return self.minio.upload_csv(csv_content, f"quotes_export_{timestamp}.csv")
    
#     def export_json(self) -> Optional[str]:
#         """Exporte toutes les données en JSON."""
#         data = self.mongodb.get_all_data()
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#         for quote in data["quotes"]:
#             if "scraped_at" in quote and isinstance(quote["scraped_at"], datetime):
#                 quote["scraped_at"] = quote["scraped_at"].isoformat()
#             if "updated_at" in quote and isinstance(quote["updated_at"], datetime):
#                 quote["updated_at"] = quote["updated_at"].isoformat()
        
#         return self.minio.upload_json(data, f"full_export_{timestamp}.json")
    
#     def create_backup(self) -> Optional[str]:
#         """Crée une sauvegarde complète."""
#         data = self.mongodb.get_all_data()

#         for quote in data["quotes"]:
#             if "scraped_at" in quote and isinstance(quote["scraped_at"], datetime):
#                 quote["scraped_at"] = quote["scraped_at"].isoformat()
#             if "updated_at" in quote and isinstance(quote["updated_at"], datetime):
#                 quote["updated_at"] = quote["updated_at"].isoformat()

#         return self.minio.create_backup(data, "quotes_backup")
    
#     ################## ANALYTICS

#     def get_analytics(self) -> dict:
#         """Génère un rapport d'analytics."""
#         return {
#             "overview": self.mongodb.get_stats(),
#             # "by_author": self.mongodb.get_quotes_by_author_stats(),
#             # "quote_lengths": self.mongodb.get_quote_length_distribution(),
#             # "author_tags": self.mongodb.get_author_tag_analysis(),
#             "storage": self.minio.get_storage_stats(),
#             "scraping_history": self.mongodb.get_scraping_history(5)
#         }

#     ################### UTILS

#     def close(self) -> None:
#         """Ferme les connexions."""
#         self.scraper.close()
#         self.mongodb.close()


# def main():
#     """Point d'entrée CLI."""
#     setup_logging("src/logs/etl-ecommerce.log", level=logging.INFO)

#     args = get_cli_args()
#     pipeline = QuotesPipeline()

    
#     try:
#         stats = pipeline.run(
#             max_pages=args.pages,
#         )
    
#      # Exports
#         if args.export_csv:
#             ref = pipeline.export_csv()
#             print(f"\nCSV exported: {ref}")
        
#         if args.export_json:
#             ref = pipeline.export_json()
#             print(f"JSON exported: {ref}")
        
#         if args.backup:
#             ref = pipeline.create_backup()
#             print(f"Backup created: {ref}")

#          # Analytics
#         analytics = pipeline.get_analytics()
#         print("\n" + "="*50)
#         print("ANALYTICS")
#         print("="*50)

#         overview = analytics.get("overview", {})
#         histories = analytics.get("scraping_history", [])
#         print(f"Total products: {overview.get('total_products', 0)}")
#         print(f"Total logs: {overview.get('total_logs', 0)}")
#         for history in histories:
#             print(f"history: {history}")
        
#     finally:
#         pipeline.close()


# if __name__ == "__main__":
#     main()


class QuotesPipeline:
    def run(self, max_pages: int = 1,):
        print("Pipeline de citations")