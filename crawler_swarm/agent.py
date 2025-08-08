"""
Crawler Swarm Agent Logic Library

This module contains pure functions for processing a webpage's HTML to
extract links and identify potential product pages.
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_all_links(base_url, html_content):
    """
    Parses the HTML content of a page and extracts all unique, absolute URLs.

    Args:
        base_url (str): The base URL of the page, used to resolve relative links.
        html_content (str): The HTML content of the page.

    Returns:
        set: A set of unique absolute URLs found on the page.
    """
    if not html_content:
        return set()

    soup = BeautifulSoup(html_content, 'lxml')
    links = set()

    for a_tag in soup.find_all('a', href=True):
        # Get the raw href attribute
        href = a_tag['href']

        # Use urljoin to build an absolute URL
        # If href is already an absolute URL, urljoin handles it correctly.
        absolute_link = urljoin(base_url, href)

        links.add(absolute_link)

    return links


# --- Heuristics for Product Page Identification ---
PRODUCT_URL_KEYWORDS = [
    '/product/',
    '/products/',
    '/item/',
    '/p/',
    '/dp/' # Amazon's detail page identifier
]

def filter_for_product_pages(urls, base_url):
    """
    Filters a set of URLs, returning only those that belong to the original
    site and are likely to be product pages.

    Args:
        urls (set): A set of absolute URLs.
        base_url (str): The base URL of the site being crawled.

    Returns:
        set: A subset of the URLs that match product page heuristics.
    """
    from urllib.parse import urlparse
    base_netloc = urlparse(base_url).netloc
    product_links = set()

    for url in urls:
        # Ensure the link belongs to the same domain before checking for keywords
        if urlparse(url).netloc != base_netloc:
            continue

        path = urlparse(url).path
        for keyword in PRODUCT_URL_KEYWORDS:
            if keyword in path:
                product_links.add(url)
                break  # Move to the next url once a keyword is found
    return product_links
