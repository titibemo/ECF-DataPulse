# import argparse
# from typing import List, Optional

# def get_cli_args():
#     """Définit et parse les arguments CLI."""
#     parser = argparse.ArgumentParser(description="Quotes Scraping Pipeline")
    
#     parser.add_argument("--pages", type=int, default=1, help="Max pages to scrape")
#     parser.add_argument("--no-authors", action="store_true", help="Skip author details")
#     parser.add_argument("--tags", nargs="+", help="Specific tags to scrape")
#     parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
#     parser.add_argument("--export-json", action="store_true", help="Export to JSON")
#     parser.add_argument("--backup", action="store_true", help="Create backup")
    
#     return parser.parse_args()


# def get_cli_args():
#     """Définit et parse les arguments CLI."""
#     parser = argparse.ArgumentParser(description="Quotes Scraping Pipeline")
    
#     parser.add_argument("--pages", type=int, default=1, help="Max pages to scrape")
#     parser.add_argument("--no-authors", action="store_true", help="Skip author details")
#     parser.add_argument("--tags", nargs="+", help="Specific tags to scrape")
#     parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
#     parser.add_argument("--export-json", action="store_true", help="Export to JSON")
#     parser.add_argument("--backup", action="store_true", help="Create backup")
    
#     return parser.parse_args()

import argparse
from typing import List, Optional
def get_cli_args():

    parser = argparse.ArgumentParser(description="Scraping / ETL Pipelines")

    parser.add_argument("--pipeline", required=True, choices=["bookspipeline", "quotespipeline"], help="Choose the pipeline to execute")
    parser.add_argument("--pages", type=int, default=1, help="Numbers of pages to scrape")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON")
    parser.add_argument("--backup", action="store_true", help="Create backup")

    return parser.parse_args()