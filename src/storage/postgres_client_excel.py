from config.settings import postgres_config
import psycopg

import structlog
logger = structlog.get_logger()


class PostgresStorage:
    """ PostgresSQL client for storing data.
    Tables :
    - partner_library
    """
    
    def __init__(self):
        self.connection_string = postgres_config.connection_string
        self.create_table()

    def _get_connection(self):
        """
        Return a connection to the PostgreSQL database.

        :return: A connection object.
        :type: psycopg2.extensions.connection
        """
        return psycopg.connect(self.connection_string)

    def create_table(self):
        
        """
        Create the partner_library table in PostgreSQL if it does not exist yet.
        
        The table has the following columns:
        - id_partner_library (INT, PRIMARY KEY, GENERATED ALWAYS AS IDENTITY)
        - name_library (VARCHAR(255), NOT NULL)
        - adresse (VARCHAR(255), NOT NULL)
        - postal_code (INT, NOT NULL)
        - city (VARCHAR(255), NOT NULL)
        - ca_by_year (INT, NOT NULL)
        - date_partnering (DATE, NOT NULL)
        - speciality (VARCHAR(255))
        - longitude (FLOAT)
        - latitude (FLOAT)
        """
        logger.info("Creating table...")

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS partner_library (
                        id_partner_library INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name_library VARCHAR(255) NOT NULL,
                        adresse VARCHAR(255) NOT NULL,
                        postal_code INT NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        ca_by_year INT NOT NULL,
                        date_partnering DATE NOT NULL,
                        speciality VARCHAR(255),
                        longitude FLOAT,
                        latitude FLOAT    
                    );
                """)

    def insert_data(self, row: dict):
        
        """
        Insert a row in the partner_library table.
        
        Args:
            row (dict): A dictionary containing the data to be inserted, with the following keys:
                - nom_librairie (str)
                - adresse (str)
                - code_postal (int)
                - ville (str)
                - ca_annuel (int)
                - date_partenariat (datetime)
                - specialite (str)
                - longitude (float)
                - latitude (float)
        """
        logger.info("Inserting data...")

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO partner_library (name_library, adresse, postal_code, city, ca_by_year, date_partnering, speciality, longitude, latitude)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        row["nom_librairie"], 
                        row["adresse"], 
                        row["code_postal"], 
                        row["ville"], 
                        row["ca_annuel"], 
                        row["date_partenariat"],
                        row["specialite"],
                        row["longitude"],
                        row["latitude"]
                    )
                )
