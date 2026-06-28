import urllib.parse
import os
from sqlalchemy import create_engine
from hrm_etl_pipeline.transform.dim_hrm_transform import *
from hrm_etl_pipeline.transform.fact_hrm_transform import *
from sqlalchemy.engine import Engine
from erp_etl_pipeline.extract.erp_extract import *
from dotenv import load_dotenv

load_dotenv()

# --- 1. CREDENTIALS & ENCODING ---
password = os.getenv('HRM_ERP_SQL_PASSWORD')
password_encode = urllib.parse.quote_plus(password)

raw_password = os.getenv('DWH_POSTGRES_PASSWORD')
encoded_password = urllib.parse.quote_plus(raw_password)

# --- 2. SQLALCHEMY URLS (Must use colons ':' for ports) ---
HRM_SQL_SERVER_CONN = (
    f"mssql+pyodbc://sa:{password_encode}@{os.getenv('HRM_SQL_SERVER_HOST')}:{os.getenv('HRM_SQL_SERVER_PORT')}/{os.getenv('HRM_SQL_SERVER_DB')}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

ERP_SQL_SERVER_CONN = (
    f"mssql+pyodbc://sa:{password_encode}@{os.getenv('ERP_SQL_SERVER_HOST')}:{os.getenv('ERP_SQL_SERVER_PORT')}/{os.getenv('ERP_SQL_SERVER_DB')}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

DW_POSTGRES_URL = (
    f"postgresql://postgres:{encoded_password}@{os.getenv('DWH_POSTGRES_HOST')}:{os.getenv('DWH_POSTGRES_PORT')}/{os.getenv('DWH_POSTGRES_DB')}"
)


# --- 3. RAW ODBC STRINGS (For pyodbc fallback only, uses commas ',') ---
HRM_RAW_ODBC = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('HRM_SQL_SERVER_HOST')},1433;"
    f"DATABASE={os.getenv('HRM_SQL_SERVER_DB')};"
    "UID=sa;"
    f"PWD={password};"       
)

ERP_RAW_ODBC = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('ERP_SQL_SERVER_HOST')},1433;"
    "DATABASE={os.getenv('ERP_SQL_SERVER_DB')};"
    "UID=sa;"
    f"PWD={password};"        
)


# --- 4. HELPER FUNCTIONS ---
def get_engine(db: str = "hrm") -> Engine:
    """Returns a SQLAlchemy Engine instance."""
    if db == "hrm":
        return create_engine(HRM_SQL_SERVER_CONN)
    elif db == "erp":
        return create_engine(ERP_SQL_SERVER_CONN)
    elif db == "postgres":
        return create_engine(DW_POSTGRES_URL)
    else:
        raise ValueError(f"Unknown database: '{db}'. Choose 'hrm', 'erp', or 'postgres'.")


def get_pyodbc_conn(db: str = "hrm"):
    """Returns a raw pyodbc connection object."""
    import pyodbc
    conn_str = ERP_RAW_ODBC if db == "erp" else HRM_RAW_ODBC
    return pyodbc.connect(conn_str)