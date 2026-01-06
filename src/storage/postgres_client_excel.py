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
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS geocoding (
                        id_geocoding INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        postcode INT NOT NULL,
                        citycode INT NOT NULL,
                        city VARCHAR(255) NOT NULL
                    );
                """)

    def library_exists(self, row: dict) -> bool:
        """
        Check if a library with the given longitude and latitude already exists in the partner_library table.

        :param row: A dictionary containing the data of the library to check.
        :type row: dict
        :return: True if the library already exists, False otherwise.
        :rtype: bool
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM partner_library
                    WHERE longitude = %s AND latitude = %s;
                    """,
                    (
                        row["longitude"],
                        row["latitude"]
                    )
                )
                return cursor.fetchone() is not None

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
        if self.library_exists(row):
            logger.info("Library already exists, skipping", name=row["nom_librairie"])
            return

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


    def geo_exists(self, properties: dict) -> bool:
        """
        Check if a library with the given citycode already exists in the geocoding table.

        :param row: A dictionary containing the data of the library to check.
        :type row: dict
        :return: True if the library already exists, False otherwise.
        :rtype: bool
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM geocoding
                    WHERE citycode = %s;
                    """,
                    (
                        properties.get("citycode"),
                    )
                )
                return cursor.fetchone() is not None

    def insert_geocoding_data(self, properties: dict):
        """
        Insert a row in the geocoding table.
        
        Args:
            row (dict): A dictionary containing the data to be inserted, with the following keys:
                - postcode (int)
                - citycode (int)
                - city (str)
        """
        if self.geo_exists(properties):
            logger.info("Geocoding already exists, skipping ")
            return

        logger.info("Inserting data in geocoding table...")

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO geocoding (postcode, citycode, city)
                    VALUES (%s, %s, %s);
                    """,
                    (
                    properties.get("postcode"),
                    properties.get("citycode"),
                    properties.get("city"),
                    )
                )


