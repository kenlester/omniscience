"""
Extractor Swarm Agent Logic Library

This module contains functions to extract structured product data from
a given webpage's HTML content. It prioritizes reliable, embedded metadata
like JSON-LD, and falls back to scraping heuristics if necessary.
"""
import re
import extruct
from bs4 import BeautifulSoup

def _extract_structured_data(url, html_content):
    """
    Uses the 'extruct' library to pull out structured data (JSON-LD, Microdata).
    """
    data = {}
    metadata = extruct.extract(html_content, base_url=url, syntaxes=['json-ld', 'microdata'])

    # JSON-LD is often the richest source
    for item in metadata.get('json-ld', []):
        if item.get('@type') == 'Product':
            data['name'] = item.get('name')
            # Look for offers, which can be a single item or a list
            offers = item.get('offers', {})
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            data['price'] = offers.get('price')
            data['currency'] = offers.get('priceCurrency')
            data['sku'] = item.get('sku')
            data['mpn'] = item.get('mpn')
            # GTIN (Global Trade Item Number) is the standard for UPCs/EANs
            data['upc'] = item.get('gtin13') or item.get('gtin12') or item.get('gtin8') or item.get('gtin')
            # We found a product, no need to look further in json-ld
            break

    # Microdata is another common format
    for item in metadata.get('microdata', []):
        if 'http://schema.org/Product' in item.get('type', []):
            props = item.get('properties', {})
            if not data.get('name'): data['name'] = props.get('name')
            if not data.get('price'): data['price'] = props.get('price')
            if not data.get('sku'): data['sku'] = props.get('sku')
            if not data.get('mpn'): data['mpn'] = props.get('mpn')
            if not data.get('upc'): data['upc'] = props.get('gtin13')
            break

    return data

def _extract_fallback_name(soup):
    """Finds the product name from the <h1> tag as a fallback."""
    if soup.h1:
        return soup.h1.get_text(strip=True)
    return None

def _extract_fallback_price(html_content):
    """Uses a regex to find a price-like pattern as a fallback."""
    # This regex looks for a currency symbol ($, €, £) followed by digits.
    # It's a simple heuristic and may not work for all sites.
    match = re.search(r'[\$€£]\s?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))', html_content)
    if match:
        return match.group(1)
    return None


def extract_product_data(url, html_content):
    """
    Extracts product information from a webpage's HTML content.

    It prioritizes structured data (JSON-LD, Microdata) and then falls back
    to scraping common HTML tags and text patterns.

    Args:
        url (str): The URL of the product page.
        html_content (str): The HTML content of the page.

    Returns:
        dict: A dictionary containing the extracted product data.
    """
    if not html_content:
        return {}

    # Primary method: Structured Data
    extracted_data = _extract_structured_data(url, html_content)

    # Fallback methods for missing data
    soup = BeautifulSoup(html_content, 'lxml')

    if not extracted_data.get('name'):
        extracted_data['name'] = _extract_fallback_name(soup)

    if not extracted_data.get('price'):
        extracted_data['price'] = _extract_fallback_price(html_content)

    # Clean up None values
    return {k: v for k, v in extracted_data.items() if v is not None}
