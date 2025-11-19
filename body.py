# email_parser/body.py

from email.message import Message
from email import message_from_string
from typing import Union

def get_text_from_email(msg: Union[Message, str]) -> str:
    """
    Extract all text/plain parts of an email.
    Accepts either:
        - email.message.Message object
        - raw string containing RFC822/MIME email content
    """

    # If a raw string is provided, convert it to a Message object.
    if isinstance(msg, str):
        msg = message_from_string(msg)

    parts = []

    for part in msg.walk():
        # Skip multipart container nodes
        if part.get_content_maintype() == "multipart":
            continue

        # Skip attachments
        if part.get_content_disposition() == "attachment":
            continue

        # Only extract plain text
        if part.get_content_type() != "text/plain":
            continue

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        charset = part.get_content_charset() or "utf-8"

        try:
            text = payload.decode(charset, errors="replace")
        except Exception:
            text = payload.decode("utf-8", errors="replace")

        parts.append(text)

    return "".join(parts).strip()

