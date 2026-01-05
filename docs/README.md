![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)
 
# **Project Name: -**  
 
## Table of Contents
 
1. [About the Project](#about-the-project)
2. [Built With](#built-with)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Project structure](#project-structure)
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
6. [Authors](#authors)
6. [License](#license)
 
---
 
## About the Project
 
This project aims to demonstrate my skills in data engineering and management by showcasing a data processing pipeline integrated. The project covers the full lifecycle of managing data, from collection to processing and storage.
This project will be update weeks by weeks until septembre 2026. 
 
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
- ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) to **containerize** the application.  
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) **Relational database** for storing structured data, providing powerful querying capabilities for efficient data retrieval and storage.  
- ![PgAdmin](https://img.shields.io/badge/PgAdmin-316192?style=for-the-badge&logo=pgadmin&logoColor=black) A **web-based tool** for managing PostgreSQL databases, used for database administration and monitoring.  
- ![Minio](https://img.shields.io/badge/Minio-1D3557?style=for-the-badge&logo=minio&logoColor=white) **Object storage** system that is compatible with Amazon S3, used for efficient file storage and management of large datasets.  
- ![GitHub](https://img.shields.io/badge/GitHub-24292F?style=for-the-badge&logo=github&logoColor=white) Used for version control and collaboration, ensuring the project remains organized and maintainable.  
- ![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) **IDE** used for development, debugging, and running the project locally.  
- ![Beautiful Soup](https://img.shields.io/badge/Beautifulsoup-000000?style=for-the-badge&logo=visualstudiocode&logoColor=white) **scrap** website.  


 
# Getting Started
 
## Prerequisites
 
Before you can install the project, make sure you have the following installed on your machine and to have basic knowledge of the following technologies:
 
- **Docker**: For containerizing the application to ensure a consistent environment.
  - [Install Docker](https://www.docker.com/products/docker-desktop/) if you don't have it already.
- **python**: In version 3.10+.
  - [Install python](https://www.python.org/downloads/) according to your operating system.


## Project structure

```bash

TODO tree /f /a

```

## Target architecture

Target architecture for scraping Quotes to Scrape :

```bash
┌─────────────────────┐
│  quotes.toscrape.com │
│                     │
│  • Citations        │
│  • Auteurs          │
│  • Tags             │
└──────────┬──────────┘
           │ Scraping
           ▼
┌─────────────────────┐
│      Scraper        │
│      Python         │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐  ┌─────────┐
│  MinIO  │  │ MongoDB │
│         │  │         │
│ Exports │  │ Quotes  │
│ Backups │  │ Authors │
│ Images  │  │ Tags    │
└─────────┘  └─────────┘
     │           │
     └─────┬─────┘
           ▼
┌─────────────────────┐
│   Analytics & NLP   │
│   ML Datasets       │
└─────────────────────┘

```

Target architecture for scraping books.toscrape.com :


```bash
┌─────────────────────┐
│  books.toscrape.com │
│                     │
│  • Titre             │
│  • prix              │
│  • note (1-5 étoiles) │
│  •  disponibilité     │
│  • catégorie         │  
└──────────┬──────────┘
           │ Scraping
           ▼
┌─────────────────────┐
│      Scraper        │
│      Python         │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐  ┌─────────┐
│  MinIO  │  │ MongoDB │
│         │  │         │
│ Exports │  │ title  │
│ Backups │  │ price │
│ Images  │  │ notation    │
│         │  │ disponibility    │
│         │  │ category    │
└─────────┘  └─────────┘
     │           │
     └─────┬─────┘
           ▼
┌─────────────────────┐
│   Analytics & NLP   │
│   ML Datasets       │
└─────────────────────┘

```

Target architecture for reaching data from the API api-adresse.data.gouv.fr :


```bash
┌─────────────────────┐
│ api-adresse.data.gouv.fr │
│                     │
    {
    "features": [{
        "geometry": {"coordinates": [2.308628, 48.850699]},
        "properties": {
        "label": "20 Avenue de Ségur 75007 Paris",
        "score": 0.95,
        "city": "Paris",
        "postcode": "75007"
        }
    }]
    }
└──────────┬──────────┘
           │ request
           ▼
┌─────────────────────┐
│      PostgresSQL with        │
│      Python         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Verification of   │
│   corresponding datas       │
└─────────────────────┘

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
    container_name: workshop-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  mongodb:
    image: mongo:7.0
    container_name: workshop-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
      MONGO_INITDB_DATABASE: scraping_db
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 30s
      timeout: 10s
      retries: 3

  mongo-express:
    image: mongo-express:latest
    container_name: workshop-mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin123
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin123@mongodb:27017/
      ME_CONFIG_BASICAUTH: false
    depends_on:
      - mongodb

volumes:
  minio_data:
  mongo_data:
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

# MinIO configuration
S3_ENDPOINT=localhost:9000       # Endpoint for MinIO server
S3_ACCESS_KEY=minioadmin         # Access key for MinIO
S3_SECRET_KEY=minioadmin123      # Secret key for MinIO
S3_SECURE=false                  # Use HTTPS (true/false)

# MongoDB configuration
MONGO_HOST=localhost             # MongoDB host
MONGO_PORT=27017                 # MongoDB port
MONGO_USER=admin                 # MongoDB username
MONGO_PASSWORD=admin123          # MongoDB password
MONGO_DB=scraping_db             # MongoDB database name

# Postgres configuration
PG_HOST=localhost                # PostgreSQL host
PG_PORT=5432                     # PostgreSQL port
PG_USER=postgres                 # PostgreSQL username
PG_PASSWORD=postgres123          # PostgreSQL password
PG_DB=scraping_db                # PostgreSQL database name

# API configuration
API_KEY=api_key            # API key for external service


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
    host: str = os.getenv("PG_HOST", "localhost")
    port: int = int(os.getenv("PG_PORT", "5432"))
    username: str = os.getenv("PG_USER", "postgres")
    password: str = os.getenv("PG_PASSWORD", "postgres123")
    database: str = os.getenv("PG_DB", "scraping_db")
```

#### MinIO
```python
@dataclass
class MinIOConfig:
    endpoint: str = os.getenv("S3_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin123")
    secure: bool = os.getenv("S3_SECURE", "false").lower() == "true"
    bucket_images:str = "author-images"
    bucket_exports:str = "quotes-exports"
    bucket_backups:str = "quotes-backups"
```

#### API
```python
@dataclass
class APIConfig:
    base_url: str = "https://example.com"
    api_key: str = os.getenv("API_KEY", "api_key")
 ```

## Usage
 
TODO
 
 
---
 
## Authors
 
- [GitHub Profile](https://github.com/titibemo)
 
---
 
## License
 
This project is open-source and can be freely copied, modified, and distributed by anyone. No specific license is provided, but contributions and usage are welcome.