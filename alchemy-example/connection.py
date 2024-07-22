import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

load_dotenv()

def get_mssql_engine():
    SQL_SERVER_HOST = os.getenv('SQL_SERVER_HOST', '127.0.0.1,1433')
    SQL_SERVER_DB = os.getenv('SQL_SERVER_DB', 'eHC')
    SQL_SERVER_USER = os.getenv('SQL_SERVER_USER', 'sa')
    SQL_SERVER_PASS = os.getenv('SQL_SERVER_PASS', 'Admin#1234')

    connection_string = (
        f'mssql+pyodbc://{SQL_SERVER_USER}:{SQL_SERVER_PASS}@{SQL_SERVER_HOST}/{SQL_SERVER_DB}'
        '?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    )

    return create_engine(connection_string)

def get_postgres_engine():
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'gkim')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'root')
    POSTGRES_PASS = os.getenv('POSTGRES_PASS', 'password')

    connection_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}/{POSTGRES_DB}'

    return create_engine(connection_string)

def get_sessions():
    mssql_engine = get_mssql_engine()
    postgres_engine = get_postgres_engine()

    MssqlSession = sessionmaker(bind=mssql_engine)
    PostgresSession = sessionmaker(bind=postgres_engine)
    return MssqlSession(), PostgresSession()

def use_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        mssql_session, postgres_session = get_sessions()
        try:
            result = func(mssql_session, postgres_session, *args, **kwargs)
        finally:
            mssql_session.close()
            postgres_session.close()
        return result
    return wrapper