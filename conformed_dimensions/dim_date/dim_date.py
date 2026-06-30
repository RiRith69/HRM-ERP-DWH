import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config.db_config import DW_POSTGRES_URL
import psycopg2
from psycopg2.extras import execute_values
from datetime import date, timedelta

START_DATE = date(2013, 1, 1)    # Inclusive — adjust as needed
END_DATE   = date(2040, 12, 31)  # Inclusive — adjust as needed
# ─────────────────────────────────────────────────────────────────────────────
# CAMBODIAN PUBLIC HOLIDAYS
# ─────────────────────────────────────────────────────────────────────────────

# Fixed-date holidays expressed as (month, day) → name.
# These apply to every year in the date range.
FIXED_HOLIDAYS: dict[tuple[int, int], str] = {
    (1,   1): "International New Year",
    (1,   7): "Victory over Genocide Day",
    (3,   8): "International Women's Day",
    (5,   1): "International Workers' Day",
    (5,  13): "King Sihamoni's Birthday",
    (5,  14): "King Sihamoni's Birthday",
    (5,  15): "King Sihamoni's Birthday",
    (6,  18): "Queen Mother's Birthday",
    (9,  24): "Constitutional Day",
    (10, 15): "King Father's Commemoration Day",
    (10, 23): "Paris Peace Agreement Day",
    (10, 29): "King's Coronation Day",
    (10, 30): "King's Coronation Day",
    (10, 31): "King's Coronation Day",
    (11,  9): "Independence Day",
    (12, 10): "International Human Rights Day",
}

# Khmer New Year — typically April 13-15 every year.
# Override specific years in this dict when the dates differ (e.g. Apr 14-16).
# Any year NOT listed here falls back to Apr 13-15.
KHMER_NEW_YEAR_OVERRIDES: dict[int, list[date]] = {
    # Example override:
    # 2027: [date(2027, 4, 14), date(2027, 4, 15), date(2027, 4, 16)],
}

# Lunar / variable holidays — extend each year from MLVT official announcements.
# Format: exact date → holiday name
# NOTE: Lunar holidays override fixed-date entries if they fall on the same date.
LUNAR_HOLIDAYS: dict[date, str] = {
    # ── 2024 ──────────────────────────────────────────────────────────────────
    date(2024,  2, 24): "Meak Bochea Day",
    date(2024,  5,  9): "Royal Ploughing Ceremony",
    date(2024,  4,  8): "Visak Bochea Day",
    date(2024,  9, 16): "Pchum Ben",
    date(2024,  9, 17): "Pchum Ben",
    date(2024,  9, 18): "Pchum Ben",
    date(2024, 11, 13): "Water Festival (Bon Om Touk)",
    date(2024, 11, 14): "Water Festival (Bon Om Touk)",
    date(2024, 11, 15): "Water Festival (Bon Om Touk)",
    # ── 2025 ──────────────────────────────────────────────────────────────────
    date(2025,  2, 12): "Meak Bochea Day",
    date(2025,  5, 21): "Royal Ploughing Ceremony",
    date(2025,  5, 12): "Visak Bochea Day",
    date(2025, 10,  2): "Pchum Ben",
    date(2025, 10,  3): "Pchum Ben",
    date(2025, 10,  4): "Pchum Ben",
    date(2025, 11,  3): "Water Festival (Bon Om Touk)",
    date(2025, 11,  4): "Water Festival (Bon Om Touk)",
    date(2025, 11,  5): "Water Festival (Bon Om Touk)",
    # ── 2026 ──────────────────────────────────────────────────────────────────
    date(2026,  3,  3): "Meak Bochea Day",
    date(2026,  5, 11): "Royal Ploughing Ceremony",
    date(2026,  5,  3): "Visak Bochea Day",
    date(2026,  9, 21): "Pchum Ben",
    date(2026,  9, 22): "Pchum Ben",
    date(2026,  9, 23): "Pchum Ben",
    # Add 2026 Water Festival once MLVT announces it.
    # ── Add future years here as MLVT publishes them ──────────────────────────
}


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# Python weekday(): 0 = Monday … 6 = Sunday  →  dim_date: 1 = Monday … 7 = Sunday
_DAY_NAMES: list[str] = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]

_MONTH_NAMES: list[str] = [
    "",           # index 0 — unused (months are 1-based)
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_KNY_DEFAULT_DAYS = (13, 14, 15)   # April 13-15


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _khmer_new_year_dates(year: int) -> list[date]:
    """Return the three Khmer New Year dates for a given year."""
    if year in KHMER_NEW_YEAR_OVERRIDES:
        return KHMER_NEW_YEAR_OVERRIDES[year]
    return [date(year, 4, day) for day in _KNY_DEFAULT_DAYS]


def build_holiday_map(start: date, end: date) -> dict[date, str]:
    """
    Return a complete mapping of  date → holiday_name  for every holiday that
    falls within [start, end].

    Priority (highest wins):
        1. Lunar holidays (most specific — from official MLVT announcements)
        2. Khmer New Year (annual, but overrideable)
        3. Fixed-date holidays
    """
    holidays: dict[date, str] = {}

    # ── 1. Fixed-date holidays ────────────────────────────────────────────────
    current = start
    while current <= end:
        key = (current.month, current.day)
        if key in FIXED_HOLIDAYS:
            holidays[current] = FIXED_HOLIDAYS[key]
        current += timedelta(days=1)

    # ── 2. Khmer New Year (overrides fixed if same date) ─────────────────────
    for year in range(start.year, end.year + 1):
        for d in _khmer_new_year_dates(year):
            if start <= d <= end:
                holidays[d] = "Khmer New Year"

    # ── 3. Lunar holidays (highest priority — overrides everything) ───────────
    for d, name in LUNAR_HOLIDAYS.items():
        if start <= d <= end:
            holidays[d] = name

    return holidays


def date_to_key(d: date) -> int:
    """Convert a date to the YYYYMMDD integer surrogate key."""
    return d.year * 10_000 + d.month * 100 + d.day


def generate_rows(start: date, end: date) -> list[tuple]:
    """
    Return a list of tuples, one per calendar day in [start, end], ordered by
    date ascending.

    Column order matches the INSERT statement and the DDL exactly:
        date_key, full_date, day_of_month, day_of_week, day_name,
        month_actual, month_name, year,
        is_weekend, is_working_day, is_holiday, holiday_name
    """
    holidays = build_holiday_map(start, end)
    rows: list[tuple] = []

    current = start
    while current <= end:
        dow         = current.weekday()        # 0 = Monday … 6 = Sunday
        is_weekend  = dow >= 5
        holiday_nm  = holidays.get(current)    # None if not a holiday
        is_holiday  = holiday_nm is not None
        is_workday  = not is_weekend and not is_holiday

        rows.append((
            date_to_key(current),           # date_key        INT
            current,                        # full_date        DATE
            current.day,                    # day_of_month     INT  (1-31)
            dow + 1,                        # day_of_week      INT  (1=Mon…7=Sun)
            _DAY_NAMES[dow],                # day_name         VARCHAR(50)
            current.month,                  # month_actual     INT  (1-12)
            _MONTH_NAMES[current.month],    # month_name       VARCHAR(50)
            current.year,                   # year             INT
            is_weekend,                     # is_weekend       BOOLEAN
            is_workday,                     # is_working_day   BOOLEAN
            is_holiday,                     # is_holiday       BOOLEAN
            holiday_nm,                     # holiday_name     VARCHAR(100) / NULL
        ))
        current += timedelta(days=1)

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# SQL
# ─────────────────────────────────────────────────────────────────────────────

_INSERT_SQL = """
INSERT INTO dim_date (
    date_key,
    full_date,
    day_of_month,
    day_of_week,
    day_name,
    month_actual,
    month_name,
    year,
    is_weekend,
    is_working_day,
    is_holiday,
    holiday_name
)
VALUES %s
ON CONFLICT (date_key) DO NOTHING;
"""

# ── Optional: DDL to create the table if it does not yet exist ────────────────
_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_date (
    date_key        INT          NOT NULL,
    full_date       DATE         NOT NULL,
    day_of_month    INT          NOT NULL,
    day_of_week     INT          NOT NULL,
    day_name        VARCHAR(50)  NOT NULL,
    month_actual    INT          NOT NULL,
    month_name      VARCHAR(50)  NOT NULL,
    year            INT          NOT NULL,
    is_weekend      BOOLEAN      NOT NULL DEFAULT FALSE,
    is_working_day  BOOLEAN      NOT NULL DEFAULT TRUE,
    is_holiday      BOOLEAN      NOT NULL DEFAULT FALSE,
    holiday_name    VARCHAR(100)          DEFAULT NULL,
    CONSTRAINT pk_dim_date  PRIMARY KEY (date_key),
    CONSTRAINT un_full_date UNIQUE      (full_date)
);
"""


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def _validate_config() -> None:
    """Fail fast with a clear error message if configuration is invalid."""
    if START_DATE > END_DATE:
        raise ValueError(
            f"START_DATE ({START_DATE}) must be on or before END_DATE ({END_DATE})."
        )
    if (END_DATE - START_DATE).days > 365 * 100:
        raise ValueError("Date range exceeds 100 years — please check START_DATE / END_DATE.")

    for d, name in LUNAR_HOLIDAYS.items():
        if not isinstance(d, date):
            raise TypeError(f"LUNAR_HOLIDAYS key is not a date object: {d!r}")
        if not name or not isinstance(name, str):
            raise ValueError(f"LUNAR_HOLIDAYS entry for {d} has an invalid name: {name!r}")


def _spot_checks(rows: list[tuple]) -> None:
    """Assert basic invariants on the generated rows."""
    row_map: dict[int, tuple] = {r[0]: r for r in rows}

    # No duplicate surrogate keys
    assert len(row_map) == len(rows), "Duplicate date_key values detected!"

    # Every row must have exactly 12 columns
    for r in rows:
        assert len(r) == 12, f"Row has {len(r)} columns (expected 12): {r}"

    # day_of_week must be 1-7
    for r in rows:
        assert 1 <= r[3] <= 7, f"day_of_week out of range: {r}"

    # month_actual must be 1-12
    for r in rows:
        assert 1 <= r[5] <= 12, f"month_actual out of range: {r}"

    # is_working_day must be False when is_weekend or is_holiday is True
    for r in rows:
        is_weekend, is_workday, is_holiday = r[8], r[9], r[10]
        if is_weekend or is_holiday:
            assert not is_workday, (
                f"is_working_day should be False for {r[1]} "
                f"(weekend={is_weekend}, holiday={is_holiday})"
            )

    # holiday_name must be non-None iff is_holiday is True
    for r in rows:
        if r[10]:   # is_holiday
            assert r[11] is not None, f"Missing holiday_name for holiday on {r[1]}"
        else:
            assert r[11] is None, f"Unexpected holiday_name '{r[11]}' on non-holiday {r[1]}"

    print("  ✓ All spot-checks passed.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("dim_date generator — Cambodia DWH")
    print("=" * 60)

    # ── 1. Validate config ────────────────────────────────────────────────────
    try:
        _validate_config()
    except (ValueError, TypeError) as exc:
        print(f"\n[ERROR] Configuration problem:\n  {exc}")
        sys.exit(1)

    # ── 2. Generate rows ──────────────────────────────────────────────────────
    print(f"\nGenerating rows for {START_DATE}  →  {END_DATE} …")
    rows = generate_rows(START_DATE, END_DATE)
    print(f"  {len(rows):,} rows generated.")

    # ── 3. Run integrity checks ───────────────────────────────────────────────
    print("\nRunning integrity checks …")
    _spot_checks(rows)

    # ── 4. Connect to PostgreSQL ──────────────────────────────────────────────
    print(f"\nConnecting to PostgreSQL {DW_POSTGRES_URL}")
    try:
        conn = psycopg2.connect(DW_POSTGRES_URL)
    except psycopg2.OperationalError as exc:
        print(f"\n[ERROR] Could not connect:\n  {exc}")
        sys.exit(1)
    print("  Connected.")

    # ── 5. Load rows ──────────────────────────────────────────────────────────
    try:
        with conn:
            with conn.cursor() as cur:
                print(f"\n  Inserting up to {len(rows):,} rows (ON CONFLICT DO NOTHING) …")
                execute_values(cur, _INSERT_SQL, rows, page_size=1_000)

        print(f"  Done. Up to {len(rows):,} rows loaded (existing dates skipped).")

    except psycopg2.Error as exc:
        print(f"\n[ERROR] Database error during load:\n  {exc}")
        sys.exit(1)
    finally:
        conn.close()
        print("\nConnection closed.")

    print("\n✓ dim_date load complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()