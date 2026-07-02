

import re

#Words we do not need because they are very common
COMMON_WORDS = [
    "the", "a", "an", "is", "are", "was", "were", "to", "of", "and",
    "in", "on", "for", "it", "this", "that", "your", "you", "at",
    "as", "with", "be", "by", "or", "we", "our", "i", "have", "will"
]

#Words that can show pressure and urgency
URGENT_WORDS = [
    "urgent", "immediately", "asap", "act now", "final notice",
    "warning", "alert", "suspended", "locked", "limited time",
    "verify now", "expire", "expires", "expired", "click here"
]

#Words that ask for private  info
PASSWORD_WORDS = [
    "password", "login", "log in", "verify your account",
    "confirm your identity", "bank details", "card details"
]

#This find website links in the email
LINK_PATTERN = re.compile(r"(https?://\S+|www\.\S+)")


def clean_text(text):
    """Clean the email text."""

    text = text.lower()

    text = LINK_PATTERN.sub(" link ", text)

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    cleaned_words = []

    for word in words:
        if word not in COMMON_WORDS:
            cleaned_words.append(word)

    return " ".join(cleaned_words)


def count_links(text):
    """Count links in the email."""
    links = LINK_PATTERN.findall(text)
    return len(links)


def find_warning_signs(text):
    """Find simple phishing warning signs."""

    text_lower = text.lower()
    signs = []

    if count_links(text) > 0:
        signs.append("Contains a link")

    for word in URGENT_WORDS:
        if word in text_lower:
            signs.append("Uses urgent language")
            break

    for word in PASSWORD_WORDS:
        if word in text_lower:
            signs.append("Asks for password or account details")
            break

    if text.count("!") >= 2:
        signs.append("Uses many exclamation marks")

    if "win" in text_lower or "prize" in text_lower or "free" in text_lower:
        signs.append("Mentions a prize or something free")

    return signs
