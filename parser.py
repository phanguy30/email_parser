# email_parser/parser.py

from typing import Union, Dict, Any, List
from email import message_from_string
from email.message import Message

from .body import get_text_from_email
from .replies import strip_reply_chain
from .headers import parse_date, parse_addrs


def parse_email(msg: Union[Message, str]) -> Dict[str, Any]:
    """
    Parse a single email.message.Message or raw RFC822 string into a flat dict.
    Works for general MIME emails.
    """

    # If the user passes a raw string, convert to Message
    if isinstance(msg, str):
        msg = message_from_string(msg)

    # --- headers ---
    message_id = msg.get("Message-ID")
    subject    = msg.get("Subject", "")
    date_raw   = msg.get("Date")
    date       = parse_date(date_raw)

    from_raw = msg.get("From", "")
    to_raw   = msg.get("To")
    cc_raw   = msg.get("Cc")

    from_addrs = parse_addrs(from_raw)
    to_addrs   = parse_addrs(to_raw)
    cc_addrs   = parse_addrs(cc_raw)

    # --- body ---
    body_raw   = get_text_from_email(msg)
    body_clean = strip_reply_chain(body_raw)

    # --- attachments ---
    attachment_names: List[str] = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            attachment_names.append(part.get_filename())

    has_attachment = len(attachment_names) > 0

    return {
        "message_id":     message_id,
        "date":           date,
        "from_raw":       from_raw,
        "from_emails":    from_addrs,
        "to_raw":         to_raw or "",
        "to_emails":      to_addrs,
        "cc_raw":         cc_raw or "",
        "cc_emails":      cc_addrs,
        "subject":        subject,
        "body_raw":       body_raw,
        "body_clean":     body_clean,
        "has_attachment": has_attachment,
        "attachments":    attachment_names,
        "n_to":           len(to_addrs),
        "n_cc":           len(cc_addrs),
    }