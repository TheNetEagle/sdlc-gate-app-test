"""Small string utilities."""

import re


def reverse(s: str) -> str:
    """Return the string reversed."""
    return s[::-1]


def slugify(text: str) -> str:
    """Convert text into a URL-safe ASCII slug."""
    text = text.strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
