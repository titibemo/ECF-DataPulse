from src.storage.postgres_client_excel import PostgresStorage
import pandas as pd
import structlog

logger = structlog.get_logger()

class ExcelPipeline:
    def __init__(self):
        self.postgres = PostgresStorage()
        pass

    def extract_excel(self):
        try:
            logger.info("fetching excel")
            datas = pd.read_excel("data/partenaire_librairies.xlsx")
            return datas
        except Exception as e:
            logger.error(f"Error fetching excel: {e}")
            return None
        
    def clean_data(self, datas):
        # drop les colonnes contact_nom	contact_email	contact_telephone
        datas = datas.drop(columns=["contact_nom", "contact_email", "contact_telephone"])
        return datas
        
    

    def run(self):
        datas = self.extract_excel()

        clean_data = self.clean_data(datas)

        # ajouter chaque ligne de l'excel dans la base de données
        for index, row in clean_data.iterrows():
            self.postgres.insert_data(row)




