thonpython
import logging
import requests
from bs4 import BeautifulSoup
from .utils_format import clean_text

class RedditParser:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; RedditScraper/1.0)"
        }

    def scrape(self):
        logging.info("Fetching page content...")
        res = requests.get(self.url, headers=self.headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        title = clean_text(self._extract_title(soup))
        description = clean_text(self._extract_description(soup))
        upvotes = clean_text(self._extract_upvotes(soup))
        comment_count = clean_text(self._extract_comment_count(soup))
        comments = self._extract_comments(soup)

        return {
            "title": title,
            "description": description,
            "upvotes": upvotes,
            "comment_count": comment_count,
            "comments": comments,
            "url": self.url
        }

    def _extract_title(self, soup):
        tag = soup.find("h1")
        return tag.text if tag else ""

    def _extract_description(self, soup):
        tag = soup.find("div", {"data-test-id": "post-content"})
        return tag.text if tag else ""

    def _extract_upvotes(self, soup):
        tag = soup.find("div", {"data-click-id": "upvote"})
        if tag:
            v = tag.find_next("div")
            return v.text if v else ""
        return ""

    def _extract_comment_count(self, soup):
        tag = soup.find("span", string=lambda x: x and "comment" in x.lower())
        return tag.text if tag else ""

    def _extract_comments(self, soup):
        comments = []
        comment_tags = soup.find_all("div", {"data-test-id": "comment"})
        for c in comment_tags:
            body = c.find("p")
            if body:
                comments.append(clean_text(body.text))
        return comments