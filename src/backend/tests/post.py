import json
import sys

import requests


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/test_post_cli.py <URL>")
        return

    page_url = sys.argv[1]
    backend_url = "http://127.0.0.1:5000/api/job"

    payload = {"url": page_url}
    response = requests.post(backend_url, json=payload)

    print("\nStatus:", response.status_code)
    try:
        print("Response JSON:\n", json.dumps(response.json(), indent=2))
    except Exception:
        print("Raw response:\n", response.text)


if __name__ == "__main__":
    main()
