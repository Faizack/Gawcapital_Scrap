#  Scraping GawCapital

## Overview
This Python script scrapes data from a website using Selenium for link extraction and BeautifulSoup for data parsing.

## Usage
1. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set the `link` variable to the target webpage URL in the `scraper.py` file.
4. Run the main script:
    ```bash
    cd src/;python main.py
    ```
5. Outputs two files: `links.csv` (scraped links) and `output.xlsx` (scraped data).

## Requirements
- Python 3.12

## Note
Ensure you have permission to scrape the website and abide by its terms of service.

---

This version includes steps for setting up a virtual environment, installing dependencies from a `requirements.txt` file, and running the main script.
