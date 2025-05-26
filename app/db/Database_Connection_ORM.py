from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class DatabaseConnectionORM:
    _engine = None
    _Session = None

    def __init__(self):
        if not DatabaseConnectionORM._engine:
            host = os.getenv('DB_HOST')
            user = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            db = os.getenv('DB_DB')

            try:
                DatabaseConnectionORM._engine = create_engine(
                    f'mysql+pymysql://{user}:{quote_plus(password)}@{host}/{db}?charset=utf8mb4',
                    pool_size=10,
                    max_overflow=20,
                    pool_timeout=30,
                    pool_recycle=1800,
                    pool_pre_ping=True
                )
                DatabaseConnectionORM._Session = sessionmaker(bind=DatabaseConnectionORM._engine)
            except Exception as e:
                print(f'Error connecting to the database: {e}')

    def get_base(self):
        return Base
    
    def get_engine(self):
        return DatabaseConnectionORM._engine

    def get_session(self):
        return DatabaseConnectionORM._Session()

    def close(self):
        if DatabaseConnectionORM._engine:
            DatabaseConnectionORM._engine.dispose()