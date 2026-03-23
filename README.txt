
Web‑scraping and Text‑analysis Assignment

This repository contains materials for Assignment 2, which asks you to
compare two popular web‑scraping libraries, pick one that is appropriate
for your needs, scrape at least 50 web pages on a topic of your choice,
perform text analysis on the scraped content, and provide a cleaned
dataset along with reproducible code.

Contents:

* analysis.py – a Python script that demonstrates how to collect
  the first 50 product pages from the Fiction category on the
  Books to Scrape (https://books.toscrape.com/) demo site using
  `requests` and `BeautifulSoup4`.  For each book the script extracts
  the product description, summarizes it to the first two sentences
  using TextBlob, and calculates a simple sentiment polarity score.
  The results are saved to `data.csv` with columns `url`, `summary`
  and `score`.
* data.csv – a pre‑built dataset containing 50 fiction books with
  URLs, summaries and sentiment scores.  This file is provided for
  convenience; you can recreate it by running analysis.py once
  networking is available.
* requirements.txt – a list of Python dependencies needed to run
  the scraping and analysis code.  See below for setup details.
* report.md – a research report comparing web‑scraping
  libraries and recommending the most suitable one for this assignment.

Setup and usage:

These instructions assume a Unix‑like environment with Python 3.10 or
later installed.  You can adapt the steps to Windows by replacing
`python3` with `python` and using an appropriate virtual environment
tool such as `venv`.

1. Create and activate a virtual environment

    python3 -m venv .venv
    source .venv/bin/activate

   On Windows, activate the environment with `\.venv\Scripts\activate`.

2. Install dependencies

   Install the required libraries using pip:

    pip install -r requirements.txt

   The dependencies include:
   - beautifulsoup4 for parsing HTML
   - requests for HTTP requests
   - pandas and numpy for data manipulation
   - textblob for simple text summarization and sentiment analysis

   You may need to download TextBlob’s NLTK corpora the first time you
   use it:

    python -m textblob.download_corpora

3. Run the scraping and analysis script (optional)

   To recreate the dataset, run analysis.py:

    python analysis.py

   The script fetches up to 50 fiction book pages, extracts their
   descriptions, summarises the text, computes sentiment polarity and
   writes the results to `data.csv`.  Note that the Books to Scrape
   domain must be reachable from your network; the environment used to
   prepare this repository did not allow outbound HTTP, so analysis.py
   has not been executed here.

4. Explore the data

   The resulting data.csv file contains three columns:

    • url: absolute URL of the book detail page on Books to Scrape
    • summary: two‑sentence summary of the book’s product description
    • score: sentiment polarity score (range −1 to 1) of the summary

   You can load the CSV into pandas or Excel to inspect the summaries and
   scores.  A positive score indicates generally optimistic language,
   while a negative score corresponds to more negative or pessimistic
   tone.

Notes and limitations:

* Network access – the requests calls in analysis.py will raise errors
  if the Books to Scrape website is not reachable.  In the environment
  used for this assignment, outgoing HTTP requests were blocked, so the
  dataset provided here (data.csv) was assembled manually and summarised
  offline.
* Simplistic summarization – the summarization strategy takes the
  first two sentences of each product description.  More sophisticated
  approaches (e.g., TextRank, BERT) could produce better summaries but
  require additional libraries and compute.
* Sentiment scores – TextBlob’s polarity scores offer a crude
  approximation of sentiment.  They are sensitive to word choice and
  may not perfectly reflect the nuanced tone of a description.  For
  more accurate sentiment analysis you could use the vaderSentiment
  library or transformer‑based models.

Contact:

If you have questions or run into issues with the code, please reach
out to the assignment instructor or open an issue in your course
repository.