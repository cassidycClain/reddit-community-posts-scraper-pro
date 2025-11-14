thonpython
import json
import logging
from pathlib import Path
from extractors.reddit_parser import RedditParser
from outputs.exporters import Exporter

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def load_input_file(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError("Input file must contain valid JSON.") from e

def main():
    logging.info("Loading input...")
    data = load_input_file("data/sample.json")
    url = data.get("url")
    if not url:
        raise ValueError("Input JSON must contain a 'url' field.")

    logging.info(f"Scraping Reddit URL: {url}")
    parser = RedditParser(url)
    result = parser.scrape()

    logging.info("Exporting data...")
    Exporter.save_json(result, "output.json")

    logging.info("Done. Output saved to output.json")

if __name__ == "__main__":
    main()