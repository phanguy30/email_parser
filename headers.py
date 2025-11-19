# email_parser/headers.py
from datetime import datetime
from email.utils import getaddresses, parsedate_to_datetime
from typing import List, Optional

def parse_date(date_raw: str | None) -> Optional[datetime]:
    """Robustly parse Date header to datetime, or return None."""
    if not date_raw:
        return None
    try:
        return parsedate_to_datetime(date_raw)
    except Exception:
        return None


def parse_addrs(field_value: Optional[str]) -> List[str]:
    """
    Given a header value from msg.get("To") / msg.get("Cc") / msg.get("From"),
    return a clean list of email addresses.

    Parameters
    ----------
    field_value : str or None
        The raw header string returned by msg.get("<header>").
        Examples:
            "John <john@example.com>, jane@corp.com"
            "boss@company.com"
            None

    Returns
    -------
    List[str]
        A list of extracted email addresses.
        Examples:
            ["john@example.com", "jane@corp.com"]
            []
    """
    if not field_value:
        return []

    pairs = getaddresses([field_value])  # list of (display_name, email)
    return [email_addr.strip() for _, email_addr in pairs if email_addr]