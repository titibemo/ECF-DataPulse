from src.storage.postgres_client_excel import PostgresStorage
from src.pipelines.pipeline_api import APIPipeline
from src.storage.minio_client import MinIOStorage
import pandas as pd
import structlog
import time
from datetime import datetime
from utils.cli_args import get_cli_args

logger = structlog.get_logger()

class ExcelPipeline:
    """Pipeline to fetch excel data, clean it, enrich it with latitude and longitude, and save it in postgreSQL."""
    
    def __init__(self):
        self.postgres = PostgresStorage()
        self.minio = MinIOStorage()
        self.api = APIPipeline()

    def extract_excel(self) -> pd.DataFrame|None:
        """ Extract the excel file and return the data as a dataframe if found else return None"""
        try:
            logger.info("fetching excel")
            datas = pd.read_excel("data/partenaire_librairies.xlsx")
            return datas
        except Exception as e:
            logger.error(f"Error fetching excel: {e}")
            return None
        
    def clean_data(self, datas: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the excel data by dropping duplicated values and dropping the columns contact_nom, contact_email and contact_telephone.
        """
        datas = datas.drop_duplicates()
        datas = datas.drop(columns=["contact_nom", "contact_email", "contact_telephone"])
        return datas
    
    
    def enrich_data(self, clean_data: pd.DataFrame, index: int, coordinates: dict) -> pd.DataFrame:
        """Add latitude and longitude to the dataframe."""

        if coordinates and coordinates["features"] and len(coordinates["features"]) > 0:
            clean_data.at[index, "latitude"] = coordinates["features"][0]["geometry"]["coordinates"][0] or "NaN"
            clean_data.at[index, "longitude"] = coordinates["features"][0]["geometry"]["coordinates"][1] or "NaN"
            return clean_data
        else:
            logger.error(f"No coordinates found for index {index}")
            clean_data.at[index, "latitude"] = ""
            clean_data.at[index, "longitude"] = ""
        return clean_data
    
    def backup_json(self):
        """Backup the excel data to MinIO before manipulation."""
        csv_content = self.extract_excel().to_csv(index=False)
        self.minio.create_backup(csv_content, "librairy_partner_export")
        logger.info("Backup created")

    def export_csv(self, data, filepath: str = None):
        """
        Export the excel data to a csv file.
        """
        # Upload vers MinIO
        data_csv = data.to_csv()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        return self.minio.upload_csv(data_csv, f"librairy_partner_export_{timestamp}.csv")

    def run(self) -> None:

        """
        Run the pipeline to fetch the data from excel and create a backup. Data will be clean it, enrich it with latitude and longitude, and print the enriched data.

        The pipeline is as follows:
        - Fetch the data from excel
        - Clean the data by dropping the columns contact_nom, contact_email and contact_telephone
        - Enrich the data by adding the latitude and longitude obtained from the French Address API
        - Save the enriched data in postgreSQL

        :return: None
        """
        args = get_cli_args()
        self.backup_json()

        datas = self.extract_excel()
        clean_data = self.clean_data(datas)

        for index, row in clean_data.iterrows():
            address = f"{row['adresse']}, {row['code_postal']} {row['ville']}"
            geo = self.api.get_geocode(address)

            data_enrich = self.enrich_data(clean_data=clean_data, index=index, coordinates=geo)

            self.postgres.insert_data(data_enrich.iloc[index])
            time.sleep(1)

        if args.export_csv:
            data_enrich.to_csv()
            self.export_csv(data=data_enrich)
            logger.info("CSV exported")






