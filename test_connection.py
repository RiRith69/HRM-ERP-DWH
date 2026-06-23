from sqlalchemy import text
from config.db_config import get_engine
from dotenv import load_dotenv

load_dotenv()

def test_connection(db_name: str, label: str):
    print(f"⏳ Testing {label}...")
    try:
        engine = get_engine(db_name)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"✅ {label} — Connection SUCCESSFUL!")
    except Exception as e:
        print(f"❌ {label} — Connection FAILED!")
        print(f"📁 Error Details: {e}")
    print("-" * 50)


print("=" * 50)
print("🔍 Initializing database connection test...")
print("=" * 50)

test_connection("hrm",      "HRM Source (SQL Server)")
test_connection("erp",      "ERP Source (SQL Server)")
test_connection("postgres", "Data Warehouse Target (PostgreSQL)")

print("🏁 Connection test run complete.")