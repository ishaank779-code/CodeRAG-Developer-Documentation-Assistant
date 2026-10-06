import re
from collections import Counter

STOPWORDS = {"the", "a", "an", "is", "are", "to", "of", "for", "in", "on", "and", "or", "with", "how", "what", "why", "can", "i", "you", "my", "from", "it", "this", "that"}

def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_+#.-]{2,}", text.lower())
    return [w for w in words if w not in STOPWORDS]

def term_counts(text: str):
    return Counter(tokenize(text))
