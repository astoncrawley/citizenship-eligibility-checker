from datetime import datetime, date
from typing import Optional

def parse_date(date_str: str) -> Optional[date]:
    """Parse a string (YYYY-MM-DD, DD/MM/YYYY, etc.) into a date object."""
    if not date_str:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")

# # Utility: build date from ISO string
# def parse_date(s: str) -> date:
#     return datetime.fromisoformat(s).date()
