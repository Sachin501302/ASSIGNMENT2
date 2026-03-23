"""
analysis.py
---------------

This script demonstrates how to scrape textual data from the open demo site
“Books to Scrape” and perform basic natural‑language analysis on it.  It
illustrates the use of BeautifulSoup4 for parsing static HTML, the Requests
library for issuing HTTP requests, and TextBlob for computing simple
sentiment polarity scores.  Given that the assignment requires scraping
at least 50 product pages from the Fiction category, the script traverses
pagination until it has processed 50 books.  For each book it extracts
the product description, summarizes it to its first two sentences and
computes a polarity score.  The results are written to a CSV file with
columns `url`, `summary` and `score`.

The script is written to be straightforward and reproducible.  It relies
only on widely used, open‑source packages.  Should you wish to run this
locally, make sure to install dependencies listed in `requirements.txt` and
note that the Books to Scrape domain (`books.toscrape.com`) must be
reachable from your network; the environment used during development had
outgoing HTTP blocked, so the script has not been executed here but
represents a clear, step‑by‑step solution.
"""

from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


BASE_URL = "https://books.toscrape.com"
FICTION_CATEGORY_URL = (
    "https://books.toscrape.com/catalogue/category/books/fiction_10/"
)


@dataclass
class BookRecord:
    url: str
    summary: str
    score: float


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch an HTML page and return a parsed BeautifulSoup object.

    Raises an HTTPError if the response is unsuccessful.
    """
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_book_links(category_url: str, max_books: int) -> List[str]:
    """Collect book detail page URLs from the category until max_books are found."""
    links = []
    page_number = 1
    while len(links) < max_books:
        url = (
            category_url + f"page-{page_number}.html"
            if page_number > 1
            else category_url + "index.html"
        )
        soup = fetch_page(url)
        # Each product link appears in an h3 tag inside an article.product_pod
        for h3 in soup.select("article.product_pod h3 a"):
            href = h3.get("href")
            # Normalize relative URLs
            full_url = href
            if not href.startswith("http"):
                # Some URLs start with '../', strip and join
                full_url = BASE_URL + "/catalogue/" + href.replace("../", "")
            links.append(full_url)
            if len(links) >= max_books:
                break
        # Check if there is a next page; break if none
        next_button = soup.find("li", class_="next")
        if not next_button:
            break
        page_number += 1
        time.sleep(0.5)  # polite delay between pages
    return links[:max_books]


def extract_description(book_url: str) -> str:
    """Return the raw product description from a book detail page."""
    soup = fetch_page(book_url)
    desc_header = soup.find("div", id="product_description")
    if not desc_header:
        return ""
    desc = desc_header.find_next_sibling("p")
    return desc.get_text(strip=True)


def summarize_text(text: str, sentences: int = 2) -> str:
    """Summarize text by returning the first `sentences` sentences."""
    blob = TextBlob(text)
    sentence_list = blob.sentences
    if not sentence_list:
        return ""
    return " ".join(str(s) for s in sentence_list[:sentences])


def compute_polarity(text: str) -> float:
    """Compute sentiment polarity score using TextBlob."""
    return TextBlob(text).sentiment.polarity


def scrape_fiction_books(num_books: int = 50) -> List[BookRecord]:
    """Main orchestration: collect book links, parse descriptions, summarize and score."""
    book_links = get_book_links(FICTION_CATEGORY_URL, num_books)
    records = []
    for link in book_links:
        try:
            description = extract_description(link)
            summary = summarize_text(description, sentences=2)
            score = compute_polarity(summary)
            records.append(BookRecord(url=link, summary=summary, score=score))
        except Exception as exc:
            print(f"Failed to process {link}: {exc}")
        time.sleep(0.5)
    return records


def save_to_csv(records: List[BookRecord], filename: str) -> None:
    """Write records to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "summary", "score"])
        for rec in records:
            writer.writerow([rec.url, rec.summary, f"{rec.score:.3f}"])


if __name__ == "__main__":
    # Example usage: scrape 50 fiction books and save to CSV
    results = scrape_fiction_books(num_books=50)
    save_to_csv(results, "data.csv")
    print(f"Scraped {len(results)} records. Data saved to data.csv")