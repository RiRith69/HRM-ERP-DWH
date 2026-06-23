import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# --- ADDED SmallInteger TO IMPORTS ---
from sqlalchemy import create_engine, MetaData, Table, Column, text, String, Boolean, LargeBinary, Numeric, DateTime, Text, SmallInteger
from sqlalchemy.engine import Engine
from config.db_config import HRM_SQL_SERVER_CONN, ERP_SQL_SERVER_CONN, DW_POSTGRES_URL

SOURCES = {
    "hrm": {"conn": HRM_SQL_SERVER_CONN, "schema": "staging_hrm"},
    "erp": {"conn": ERP_SQL_SERVER_CONN, "schema": "staging_erp"},
}

STAGING_CONN = DW_POSTGRES_URL
staging_engine = create_engine(STAGING_CONN)


def sync_source_schema(source_name, source_conn_or_engine, staging_schema, tables=None):
    """
    Reflect tables from SQL Server and safely rebuild them for PostgreSQL by
    cleaning up incompatible collations and translating vendor-specific types.
    """
    if isinstance(source_conn_or_engine, Engine):
        source_engine = source_conn_or_engine
    else:
        print(f"[{source_name}] Connecting to source database...")
        source_engine = create_engine(source_conn_or_engine)

    source_meta = MetaData()
    source_meta.reflect(bind=source_engine, only=tables)

    # Ensure target schema exists in PostgreSQL
    with staging_engine.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{staging_schema}"'))

    staging_meta = MetaData(schema=staging_schema)
    
    for table_name, src_table in source_meta.tables.items():
        columns = []
        
        for c in src_table.columns:
            col_type = c.type
            type_name = type(col_type).__name__.upper()
            
            # --- Robust Data Type Translation ---
            
            # 1. Map SQL Server BIT to clean Boolean
            if type_name == "BIT":
                col_type = Boolean()
            
            # 2. CRITICAL FIX: Map SQL Server TINYINT to clean SmallInteger for Postgres
            elif type_name == "TINYINT":
                col_type = SmallInteger()
                
            # 3. Map SQL Server binary types (VARBINARY, BINARY, IMAGE) to clean Postgres LargeBinary (BYTEA)
            elif "BINARY" in type_name or type_name == "IMAGE":
                col_type = LargeBinary()
                
            # 4. Map SQL Server Unicode strings (NVARCHAR, NCHAR) to safe Postgres String/VARCHAR
            elif "NVARCHAR" in type_name or "NCHAR" in type_name:
                length = getattr(col_type, "length", None)
                col_type = String(length)
                
            # 5. Handle SQL Server TEXT/NTEXT types which might have lengths that break Postgres
            elif type_name == "TEXT" or type_name == "NTEXT":
                col_type = Text()
                
            # 6. Handle sysname and unknown/NULL fallbacks
            elif type_name == "SYSNAME" or str(col_type).upper() == "NULL":
                col_type = String(256)
                
            # 7. Handle money and datetimes safely
            elif "MONEY" in type_name:
                col_type = Numeric(19, 4)
            elif "DATETIME" in type_name:
                col_type = DateTime()
            
            # --- Remove SQL Server Collations ---
            if hasattr(col_type, "collation") and col_type.collation is not None:
                col_type.collation = None

            # Append the cleaned and mapped column structure
            columns.append(
                Column(c.name, col_type, nullable=c.nullable)
            )
            
        Table(f"stg_{table_name}", staging_meta, *columns)

    if source_meta.tables:
        staging_meta.create_all(staging_engine, checkfirst=True)
        print(f"[{source_name}] Successfully synced {len(source_meta.tables)} table(s) into schema '{staging_schema}'\n")
    else:
        print(f"[{source_name}] No tables found to sync.\n")


if __name__ == "__main__":
    print("Starting DWH Staging Schema Synchronization...\n")
    
    for name, info in SOURCES.items():
        try:
            sync_source_schema(name, info["conn"], info["schema"])
        except Exception as e:
            print(f"ERROR: Failed to sync source system '{name}' due to:\n{e}\n")
            
    print("Staging synchronization task finalized.")