"""Main script, Choosing the pipeline and the options (Exports, backup...)."""

#import structlog

#pipelines
from src.pipelines.pipeline_quotes import QuotesPipeline
from src.pipelines.pipeline_books import BooksPipeline

#logging
from utils.logger import setup_logging
import logging

# cli
from utils.cli_args import get_cli_args

PIPELINES = {
    "quotespipeline": QuotesPipeline,
    "bookspipeline": BooksPipeline,
}


def main():
    """Point d'entrée CLI."""
    setup_logging("src/logs/etl-ecommerce.log", level=logging.INFO)

    args = get_cli_args()
    
    pipeline_cls = PIPELINES.get(args.pipeline)
    if not pipeline_cls:
        raise ValueError(f"Pipeline inconnue: {args.pipeline}")

    pipeline = pipeline_cls()

    
    try:
        stats = pipeline.run(
            max_pages=args.pages,
        )
    
     # Exports
        if args.export_csv:
            ref = pipeline.export_csv()
            print(f"\nCSV exported: {ref}")
        
        if args.export_json:
            ref = pipeline.export_json()
            print(f"JSON exported: {ref}")
        
        if args.backup:
            ref = pipeline.create_backup()
            print(f"Backup created: {ref}")

         # Analytics
        # analytics = pipeline.get_analytics()
        # print("\n" + "="*50)
        # print("ANALYTICS")
        # print("="*50)

        # overview = analytics.get("overview", {})
        # histories = analytics.get("scraping_history", [])
        # print(f"Total products: {overview.get('total_products', 0)}")
        # print(f"Total logs: {overview.get('total_logs', 0)}")
        # for history in histories:
        #     print(f"history: {history}")
        
    finally:
        pipeline.close()
        print("FINI")


if __name__ == "__main__":
    main()


# PIPELINES = {
#     "pipeline1": QuotesPipeline,
#     # "pipeline2": ProductsPipeline,
# }

# def main():
#     setup_logging("src/logs/etl-ecommerce.log", level=logging.INFO)

#     args = get_cli_args()

#     pipeline_cls = PIPELINES.get(args.pipeline)
#     if not pipeline_cls:
#         raise ValueError(f"Pipeline inconnue: {args.pipeline}")

#     pipeline = pipeline_cls()

#     try:
#         pipeline.run(
#             max_pages=args.pages,
#         )

#         if args.export_csv:
#             pipeline.export_csv()

#         if args.export_json:
#             pipeline.export_json()

#         if args.backup:
#             pipeline.create_backup()

#     finally:
#         print("FINI")

# if __name__ == "__main__":
#     main()