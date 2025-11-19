# email_parser/replies.py
import re

_REPLY_PATTERNS = [
    # Common separators
    r"^-{2,}\s*Original Message\s*-{2,}\s*$",
    r"^-{2,}\s*Forwarded Message\s*-{2,}\s*$",
    r"^-{2,}\s*Forwarded to.*-{2,}\s*$",

    # Gmail-style reply line
    r"^[>\s]*On .+wrote:\s*$",

    # Header-style quoted sections
    r"^[>\s]*From:\s+.+@.+$",
    r"^[>\s]*To:\s+.*@.*$",
    r"^[>\s]*Cc:\s+.*@.*$",
]

_RE_REPLY_SPLITTER = re.compile(
    "|".join(_REPLY_PATTERNS),
    flags=re.IGNORECASE | re.MULTILINE
)

def strip_reply_chain(text: str) -> str:
    """Return the part of the email before the first reply separator."""
    if not isinstance(text, str):
        return text

    match = _RE_REPLY_SPLITTER.search(text)
    if match:
        return text[:match.start()].strip()

    return text.strip()