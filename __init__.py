# email_parser/__init__.py
from .parser import parse_email
from .body import get_text_from_email
from .replies import strip_reply_chain

__all__ = ["parse_email", "get_text_from_email", "strip_reply_chain"]