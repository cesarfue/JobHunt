import json
import sys

import requests
from bs4 import BeautifulSoup


def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/test_post_cli.py <URL>")
        return

    page_url = sys.argv[1]
    print(f"Fetching page: {page_url}")

    resp = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    page_content = extract_visible_text(resp.text)
    soup = BeautifulSoup(resp.text, "html.parser")
    page_title = soup.title.string.strip() if soup.title else "Untitled"

    data = {
        "content": page_content,
        "title": page_title,
        "url": page_url,
    }

    backend_url = "http://127.0.0.1:5000/api/job"
    print(f"Sending POST to {backend_url} ...")
    response = requests.post(backend_url, json=data)

    print("\nStatus:", response.status_code)
    try:
        print("Response JSON:\n", json.dumps(response.json(), indent=2))
    except Exception:
        print("Raw response:\n", response.text)


if __name__ == "__main__":
    main()
