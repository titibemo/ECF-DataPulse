![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)
 
# **Project Name: ECF - DATAPULSE-MULTISOURCES**  
 
## Table of Contents
 
1. [About the Project](#about-the-project)
2. [Built With](#built-with)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Project structure](#project-structure)
   - [Target architecture](#target-architecture)
        -   [Scraping Quotes to Scrape](#quotes-to-scrape)
        -   [Scraping books to Scrape](#books-to-scrape)
        -   [API api-adresse.data.gouv.fr](#api)
4. [Installation and configuration](#installation-and-configuration)
   - [Installation](#installation)
   - [Configuration](#configuration)
        -   [Docker-compose](#docker-compose)
        -   [Database client](#database-client)
            - [MongoDB](#mongodb)
            - [Postgresql](#postgresql)
            - [MinIO](#minIO)
        - [Api](#api)
5. [Usage](#usage)
   - [CLI arguments](#cli-arguments)
   - [Books pipeline](#books-pipeline)
   - [Quotes Pipeline](#quotes-pipeline)
   - [Excel pipeline](#excel-pipeline)
6. [Authors](#authors)
7. [License](#license)
 
---
 
## About the Project
 
This project aims to demonstrate my skills in data engineering and management by showcasing a data processing pipeline integrated. The project covers the full lifecycle of managing data, from collection to processing and storage.
 
### **Project goals include:**  
 
- Designing a data infrastructure (data lake / data warehouse).
- Collecting data from multiple sources.
- Cleaning, transforming, and organizing data through ETL (Extract, Transform, Load) processes.
- Storing data reliably and efficiently.
- Developing a structured data pipeline in Python.
- Industrializing the solution (making it reproducible, deployable, and maintainable).
- Managing a complete data project in a professional context, from end-to-end.
 
---
 
## Built With
 
The following technologies are used in this project:
 
https://github.com/inttter/md-badges


- ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) **Version 3.14**  
- ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) Used to **containerize** the application and ensure a consistent runtime environment.  
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) **Relational database** used to store structured data.  
- ![PgAdmin](https://img.shields.io/badge/PgAdmin-316192?style=for-the-badge&logo=pgadmin&logoColor=black) A **web-based administration tool** for managing and monitoring PostgreSQL databases.  
- ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) **NoSQL document-oriented database** used to store semi-structured data.  
- ![Mongo Express](https://img.shields.io/badge/Mongo%20Express-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) A **web-based MongoDB administration interface** used to visualize, explore, and manage MongoDB collections and documents.  
- ![MinIO](https://img.shields.io/badge/MinIO-1D3557?style=for-the-badge&logo=minio&logoColor=white) **Object storage system** compatible with Amazon S3, used for efficient storage and management of files and large datasets.  
- ![GitHub](https://img.shields.io/badge/GitHub-24292F?style=for-the-badge&logo=github&logoColor=white) Used for **version control and collaboration**, ensuring the project remains organized and maintainable.  
- ![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) **IDE** used for development, debugging, and running the project locally.  
- ![Beautiful Soup](https://img.shields.io/badge/BeautifulSoup-000000?style=for-the-badge) **Web scraping library** used to extract data from websites.

 
# Getting Started
 
## Prerequisites
 
Before you can install the project, make sure you have the following installed on your machine and to have basic knowledge of the following technologies:
 
- **Docker**: For containerizing the application to ensure a consistent environment.
  - [Install Docker](https://www.docker.com/products/docker-desktop/) if you don't have it already.
- **python**: In version 3.10+.
  - [Install python](https://www.python.org/downloads/) according to your operating system.


## Project structure

Complete project structure :

```bash

project-root/
├── .venv/                         # Python virtual environment (not versioned)
│
├── config/
│   └── settings.py                # Configuration for MongoDB, Mongo Express,
│                                  # PostgreSQL, PgAdmin and external APIs
│
├── consigne/
│   └── ECF-DataPulse-MultiSources.md
│                                  # Official project instructions
│
├── data/
│   └── partenaire_librairies.xlsx # Partner libraries data used for geocoding
│                                  # via the Adresse API
│
├── docs/
│   ├── DAT.md                     # Technical Architecture Document (TAD)
│   └── RGPD_CONFORMITE.md          # GDPR compliance documentation
│
├── sql/
│   └── analyses.sql               # Analytical SQL queries
│
├── src/
│   ├── pipelines/
│   │   ├── pipeline_api.py        # Adresse API pipeline (used with Excel data)
│   │   ├── pipeline_books.py      # Books pipeline (scraping books.toscrape.com)
│   │   ├── pipeline_excel.py      # Excel pipeline (transform & load partner
│   │   │                          # data into PostgreSQL)
│   │   └── pipeline_quotes.py     # Quotes pipeline (scraping quotes data)
│   │
│   ├── scrapers/
│   │   ├── scraper_books.py       # Web scraper for books
│   │   └── scraper_quotes.py      # Web scraper for quotes
│   │
│   ├── storage/
│   │   ├── mongo_client_books.py  # MongoDB client for books data
│   │   ├── mongo_client_quotes.py # MongoDB client for quotes data
│   │   └── postgres_client_excel.py # PostgreSQL client for partner libraries
│   
├── utils/
│   └── cli_args.py                # Command-line arguments to select pipelines
│                                  # and execution options
│
├── main.py                        # Application entry point
│
├── docker-compose.yml             # Docker services (PostgreSQL, MongoDB,
│                                  # Mongo Express, PgAdmin, MinIO)
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview and usage instructions
└── .gitignore                     # Files and folders excluded from Git


```

## Target architecture

Every target get some additionnal features with minIO, these features are available with the cli arguments options.
   - [CLI arguments](#cli-arguments)


### Scraping Quotes to Scrape

```bash
┌─────────────────────┐
│  quotes.toscrape.com │
│                     │
│  • quotes           │
│  • authors          │
│  • tags             │
└──────────┬──────────┘
           │ Scraping
           ▼
┌─────────────────────┐
│      Scraper        │
│      Python         │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │Save
     ▼           ▼
┌─────────┐  ┌─────────┐
│  MinIO  │  │ MongoDB │
│         │  │         │
│         │  │         │
│ Exports │  │ Quotes  │
│ Backups │  │ Authors │
│ Images  │  │ Tags    │
(optionnal)│ │         │
│         │  │         │
└─────────┘  └─────────┘
     │           │
     │           │
     └─────┬─────┘
           ▼
┌─────────────────────┐
│   Analytics & NLP   │
│   ML Datasets       │
└─────────────────────┘

```

### Scraping books to Scrape

```bash
┌─────────────────────┐
│  books.toscrape.com │
│                     │
│  • title            │
│  • price            │
│  • rating           │
│  •  availability    │
│  • category         │  
│  • picture          │  
└──────────┬──────────┘
           │ Scraping
           ▼
┌─────────────────────┐
│      Scraper        │
│      Python         │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │save
     ▼           ▼
┌─────────┐  ┌─────────┐
│  MinIO  │  │ MongoDB │
│         │  │         │
│         │  │ title   │
│ Images  │  │ price   │
│         │  │ notation│
│         │  │ disponibility    │
│         │  │ category│
└─────────┘  └─────────┘
     │           │
     └─────┬─────┘
           ▼
┌─────────────────────┐
│   Analytics & NLP   │
│   ML Datasets       │
└─────────────────────┘

```
### API api-adresse.data.gouv.fr


```bash
┌──────────────────────────────────────────────┐
│   Load partner libraries data (Excel)        │
│                using Pandas                  │
│        partenaire_librairies.xlsx            │
└───────────────────────┬──────────────────────┘
                        │
                        │ Create backup (CSV)
                        ▼
            ┌──────────────────────────┐
            │          MinIO            │
            │                          │
            │        Backups            │
            │   (original Excel data)  │
            └───────────────┬──────────┘
                            │
                            │ Data cleaning & GDPR compliance
                            │ - Remove personal data
                            │ - Normalize addresses
                            ▼
┌──────────────────────────────────────────────┐
│         French Address API                   │
│         api-adresse.data.gouv.fr             │
│                                              │
│  Example response:                           │
│  {                                           │
│    "features": [{                            │
│      "geometry": {                           │
│        "coordinates": [2.308628, 48.850699]  │
│      },                                      │
│      "properties": {                         │
│        "label": "20 Avenue de Ségur           │
│                  75007 Paris",                │
│        "score": 0.95,                         │
│        "city": "Paris",                       │
│        "postcode": "75007"                    │
│      }                                       │
│    }]                                        │
│  }                                           │
└─────────────────┬────────────────────────────┘
          ┌───────┴───────────┐
          │   Data enrichment │
          │ (latitude &       │
          │  longitude)       │
          ▼                   ▼
  ┌────────────────┐   ┌──────────────────────┐
  │      MinIO     │   │      PostgreSQL       │
  │                │   │                      │
  │                │   │  partner_libraries   │
  │   Exports      │   │                      │
  │(csv optional)  │   │  - name_library      │
  │                │   │  - adresse           │
  └────────────────┘   │  - postal_code       │
                        │  - city              │
                        │  - ca_by_year        │
                        │  - date_partnering   │
                        │  - speciality        │
                        │  - longitude         │
                        │  - latitude          │
                        └─────────────_─┬───────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────┐
│        Analytics / NLP / ML Datasets         │
│   SQL analytics & future data exploitation  │
└──────────────────────────────────────────────┘



```

we will save the data from our file partenaire_librairies.xlsx inside PostgresSQL, theses datas are structured. we can easily retreive or get some information.


# Installation and configuration

## Installation
 
To install and set up the project, follow these steps:
 
1. Clone the repository:
```bash
git clone https://github.com/your-username/project-name.git
```

2. Create a virtual environment to isolate dependencies : Navigate to the project root, open a terminal and run the followinf commands:
```bash
# On windows
python3 -m venv venv 
venv\Scripts\activate         
```

Install the required packages :
```bash
pip install -r requirements.txt  
```
 
## Configuration

### Docker-compose

```yml
services:
  minio:
    image: minio/minio:latest
    container_name: ecf1-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    command: server /data --console-address ":9001"
    volumes:
      - minio_data_ecf:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  mongodb:
    image: mongo:7.0
    container_name: ecf1-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
      MONGO_INITDB_DATABASE: scraping_db
    volumes:
      - mongo_data_ecf:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3

  mongo-express:
    image: mongo-express:latest
    container_name: ecf1-mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin123
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin123@mongodb:27017/
      ME_CONFIG_BASICAUTH: false
    depends_on:
      - mongodb

  ecf1-postgre:
    image: postgres:latest
    container_name: ecf1-postgre
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_USER: tata
      POSTGRES_DB: scraping_db
    restart: always
    volumes:
      - local_pgdata_ecf:/var/lib/postgresql
      - ./scripts_init:/docker-entrypoint-initdb.d
    ports:
      - "8001:5432"
    networks:
      - db_network

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin_gui
    depends_on:
      - ecf1-postgre
    environment:
      PGADMIN_DEFAULT_EMAIL: a@a.fr
      PGADMIN_DEFAULT_PASSWORD: secret
      PMA_HOST: ecf1-postgre
    ports:
      - "8002:80"
    volumes:
      - pgadmin-data_ecf:/var/lib/pgadmin
    networks:
      - db_network

volumes:
  minio_data_ecf:
  mongo_data_ecf:
  local_pgdata_ecf:
  pgadmin-data_ecf:

networks:
  db_network:

```

### Database client

The configuration of the database clients is located in the settings.py file inside the config folder:
```bash
config/settings.py
```
By default, some values are already set using the os.getenv(environment_variable, default_value) method.
To add your own environment variables, create a .env file at the root of the project and specify the following values:

```bash
### Configuration with example

# ===== MinIO =====
S3_ENDPOINT=localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123
S3_SECURE=false

# ===== MongoDB =====
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=admin123
MONGO_DB=scraping_db

# ===== PostgreSQL =====
POSTGRES_HOST=localhost
POSTGRES_PORT=8001
POSTGRES_USER=tata
POSTGRES_PASSWORD=secret
POSTGRES_DB=scraping_db

# ===== pgAdmin =====
PGADMIN_DEFAULT_EMAIL=a@a.fr
PGADMIN_DEFAULT_PASSWORD=secret

# ===== API configuration if needed =====
API_KEY=api_key

```

#### MongoDB
```python
@dataclass
class MongoDBConfig:
    host: str = os.getenv("MONGO_HOST", "localhost")
    port: int = int(os.getenv("MONGO_PORT", "27017"))
    username: str = os.getenv("MONGO_USER", "admin")
    password: str = os.getenv("MONGO_PASSWORD", "admin123")
    database: str = os.getenv("MONGO_DB", "scraping_db")
```

#### Postgresql
```python
@dataclass
class PostgresConfig:
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", "8001"))
    username: str = os.getenv("POSTGRES_USER", "tata")
    password: str = os.getenv("POSTGRES_PASSWORD", "secret")
    database: str = os.getenv("POSTGRES_DB", "scraping_db")
```

#### MinIO
```python
@dataclass
class MinIOConfig:
    endpoint: str = os.getenv("S3_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin123")
    secure: bool = os.getenv("S3_SECURE", "false").lower() == "true"
    bucket_images:str = "images"
    bucket_exports:str = "exports"
    bucket_backups:str = "backups"
```

#### API
```python
@dataclass
class APIConfig:
    base_url: str = "https://api-adresse.data.gouv.fr/"
    api_key: str = os.getenv("API_KEY", "")
 ```

## Usage

The application entry point is main.py. From the project root, open a terminal and run:

```bash
python main.py --pipelines name_pipeline --OPTIONS NAME_OPTIONS
```

**NOTE:** By default, scraping pipelines process 2 pages. To scrape more (or fewer) pages, use the --pages option.

```bash
#example
python main.py --pipelines bookspipeline --pages 1
```

### CLI arguments

All command-line options are defined in utils/cli_args.py. It adds additionnal options: 

```python
    # Global (required)
    parser.add_argument("--pipeline", required=True, choices=["bookspipeline", "quotespipeline", "excelpipeline"], help="Choose the pipeline to execute")

    #Scraping options (Books & Quotes)
    parser.add_argument("--pages", type=int, default=2, help="Numbers of pages to scrape")

    # Quotes pipeline specific options
    parser.add_argument("--no-authors", action="store_true", help="Skip author details")
    parser.add_argument("--tags", nargs="+", help="Specific tags to scrape")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON")
    parser.add_argument("--backup", action="store_true", help="Create backup")

    # Excel pipeline specific options
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
```

**You can retreive the options with the following commands:**
```bash
python main.py --help
```

### Books pipeline

To launch the books pipeline, launche this command :

```bash
# basic example
python main.py --pipelines bookspipeline

# example with options
python main.py --pipeline bookspipeline --pages 10

```

### Quotes Pipeline 

Scrapes quotes (and optionally authors) from https://quotes.toscrape.com :

```bash
# basic example
python main.py --pipelines quotespipeline

 #example with options
python main.py --pipeline quotespipeline --pages 5 --tags love life --export-json
```

### Excel pipeline

Loads partner libraries data from Excel, cleans it for GDPR compliance, enriches addresses using the French Address API, and stores the result in PostgreSQL.

**NOTE**: A backup is automatically created to prevent accidental data loss and allow recovery of the original dataset.

```bash
python main.py --pipelines excelpipeline
```

---
 
## Authors
 
- [GitHub Profile](https://github.com/titibemo)
 
---
 
## License
 
This project is open-source and can be freely copied, modified, and distributed by anyone. No specific license is provided, but contributions and usage are welcome.