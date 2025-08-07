"""
Discovery Swarm Agent Logic Library

This module contains pure functions for processing data related to discovering
e-commerce sites. It does not perform any I/O or tool calls itself.
"""
import re
from urllib.parse import urlparse

# --- Configuration ---
ECOMMERCE_KEYWORDS = [
    "add to cart", "checkout", "my account", "shopping bag",
    "sale", "categories", "products", "new arrivals",
    "customer service", "shipping", "returns", "wishlist", "track order"
]
KEYWORD_THRESHOLD = 3

# --- Pure Functions ---

def get_root_domain(url):
    """Extracts the root domain (e.g., 'http://www.example.com') from a URL."""
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return f"{parsed_url.scheme}://{parsed_url.netloc}"
    except Exception:
        return None
    return None

def extract_urls_from_search_results(search_results_text):
    """Extracts a list of unique root domains from the raw text of a search result."""
    found_urls = re.findall(r'https?://[^\s/$.?#].[^\s]*', search_results_text)
    root_domains = set()
    for url in found_urls:
        root_domain = get_root_domain(url)
        if root_domain:
            root_domains.add(root_domain)
    return list(root_domains)

def analyze_content_for_keywords(content):
    """Analyzes website content text and returns True if it meets the e-commerce keyword threshold."""
    if not content:
        return False
    content_lower = content.lower()

    found_keywords = 0
    for keyword in ECOMMERCE_KEYWORDS:
        if keyword in content_lower:
            found_keywords += 1

    return found_keywords >= KEYWORD_THRESHOLD
