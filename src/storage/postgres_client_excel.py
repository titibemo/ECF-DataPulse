from config.settings import postgres_config
import psycopg

import structlog
logger = structlog.get_logger()


class PostgresStorage:
    def __init__(self):
        self.connection_string = postgres_config.connection_string

    def _get_connection(self):
        return psycopg.connect(self.connection_string)

    def create_table(self):
        logger.info("Creating table...")

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS partner_librairy (
                        id_partner_librairy INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name_librairy VARCHAR(255) NOT NULL,
                        adresse VARCHAR(255) NOT NULL,
                        postal_code INT NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        ca_by_year INT NOT NULL,
                        date_partnering DATE NOT NULL,
                        speciality VARCHAR(255)    
                    );
                """)

    def insert_data(self, row: dict):
        logger.info("Inserting data...")

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO partner_librairy (name_librairy, adresse, postal_code, city, ca_by_year, date_partnering, speciality)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        row["name_librairy"], 
                        row["adresse"], 
                        row["postal_code"], 
                        row["city"], 
                        row["ca_by_year"], 
                        row["date_partnering"],
                        row["speciality"])
                )
