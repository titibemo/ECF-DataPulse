"""Main script, Choosing the pipeline and the options (Exports, backup...)."""

#import structlog

#pipelines
from src.pipelines.pipeline_quotes import QuotesPipeline
from src.pipelines.pipeline_books import BooksPipeline
from src.pipelines.pipeline_api import APIPipeline
from src.pipelines.pipeline_excel import ExcelPipeline

#logging
import structlog
logger = structlog.get_logger()

# cli
from utils.cli_args import get_cli_args

PIPELINES = {
    "quotespipeline": QuotesPipeline,
    "bookspipeline": BooksPipeline,
    "excelpipeline": ExcelPipeline,
}


def main():
    """
    Main script, selecting the pipeline and the options (Exports, backup...).
    
    Pipeline execution workflow :
    1. Parse command-line arguments
    2. Select the pipeline based on the command-line argument
    3. Run the selected pipeline

    :raises ValueError: If the pipeline is unknown
    :return: None
    """
    logger.info("========== Starting pipeline ============")

    args = get_cli_args()
    
    pipeline_cls = PIPELINES.get(args.pipeline)
    if not pipeline_cls:
        raise ValueError(f"Pipeline inconnue: {args.pipeline}")

    pipeline = pipeline_cls()
    
    try:
        if pipeline_cls != ExcelPipeline:
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

        else:
            pipeline.run()

        
    finally:
        if pipeline_cls != ExcelPipeline:
            pipeline.close()
        logger.info("========== Pipeline completed ============")


if __name__ == "__main__":
    main()
