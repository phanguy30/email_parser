# Email Parser

This module provides a simple email parser.

The main entry point is `parse_email`, which takes an email message object and:

- Extracts standard header fields (e.g., `From`, `To`, `Cc`, `Bcc`, `Subject`, `Date`, `Message-ID`).
- Retrieves the plain-text body, ignoring attachments and HTML-only content when possible.
- Strips out quoted reply chains and signatures to produce a cleaned main body.
- Collects basic attachment metadata (filename, content type, size) without inlining attachment content.

`parse_email` returns a dictionary with clearly labeled fields, for example:

- `headers`: a dict of all raw headers  
- `subject`: normalized subject line  
- `from`, `to`, `cc`, `bcc`: parsed address lists  
- `body_raw`: full text body before cleaning  
- `body_clean`: main body text with reply chains removed  
- `attachments`: list of attachment metadata
