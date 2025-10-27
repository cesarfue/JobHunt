import sqlite3

import requests
from bs4 import BeautifulSoup

from db.db import insert_jobs
from scraper.score import retrieve_job_score


def fetch_job_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def parse_job_html(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1")
    title = title.get_text(strip=True) if title else ""

    company = soup.find("div", class_="company")
    company = company.get_text(strip=True) if company else ""

    location = soup.find("div", class_="location")
    location = location.get_text(strip=True) if location else ""

    if "linkedin" in url:
        site = "linkedin"
    elif "indeed" in url:
        site = "indeed"
    else:
        site = "other"

    job_type_tag = soup.find("span", class_="job-type")
    job_type = job_type_tag.get_text(strip=True) if job_type_tag else ""
    score = retrieve_job_score(title)

    return {
        "title": title,
        "company": company,
        "location": location,
        "site": site,
        "job_url": url,
        "job_type": job_type,
        "score": score,
    }


def add_job_entry(url):
    html = fetch_job_page(url)
    if not html:
        print(f"Failed to fetch job page: {url}")
        return False

    job = parse_job_html(html, url)
    insert_jobs([job])
    print(f"Added job: {job['title']} from {url}")
    return True
